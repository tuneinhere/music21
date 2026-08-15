import asyncio
import time
import random
from typing import Dict, Tuple, List
from datetime import datetime, timezone, timedelta

from pyrogram import filters
from pyrogram.enums import ButtonStyle
from pyrogram.enums import ChatMembersFilter, ParseMode
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from Melody import app

# ── Constants ──────────────────────────────────────────────────────────────────
TG_MAX_LENGTH = 4096    
MAX_BATCH_SIZE = 20     
SLEEP_BETWEEN = 2       
AUTO_DELETE_DELAY = 60  
_PER_MENTION_EST = 52

EMOJI = [
    "🦋🦋🦋🦋🦋", "🧚🌸🧋🍬🫖", "🥀🌷🌹🌺💐", "🌸🌿💮🌱🌵", "❤️💚💙💜🖤",
    "🍔🦪🍛🍲🥗", "🍎🍓🍒🍑🌶️", "🧋🥤🧋🥛🍷", "🍬🍭🧁🎂🍡", "🍨🧉🍺☕🍻"
]

# ── State & Memory ─────────────────────────────────────────────────────────────
TASKS: Dict[int, asyncio.Task] = {}          # Menyimpan task per chat untuk cancel instan
MSG_IDS_TO_DELETE: Dict[int, List[int]] = {} # Menyimpan ID pesan tagall untuk tombol Hapus
_admin_cache: Dict[int, Tuple[float, set]] = {}
_ADMIN_CACHE_TTL = 60  

# Konfigurasi Waktu WIB (UTC+7)
WIB = timezone(timedelta(hours=7))

# Storage History Tagall
history_state = {
    "date": datetime.now(WIB).date(),
    "data": {}  # Format: {chat_id: [{"time": "12:00:00", "link": "https://t.me/..."}]}
}

# ── Helpers ────────────────────────────────────────────────────────────────────
def clean_text(text: str) -> str:
    if not text:
        return ""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

async def get_admins(chat_id: int) -> set:
    now = time.monotonic()
    cached = _admin_cache.get(chat_id)
    if cached and (now - cached[0]) < _ADMIN_CACHE_TTL:
        return cached[1]
    
    admin_ids = {
        m.user.id
        async for m in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS)
        if not m.user.is_bot
    }
    _admin_cache[chat_id] = (now, admin_ids)
    return admin_ids

async def is_admin(chat_id: int, user_id: int) -> bool:
    return user_id in await get_admins(chat_id)

async def _auto_delete(msg: Message, delay: int = AUTO_DELETE_DELAY):
    await asyncio.sleep(delay)
    try:
        await msg.delete()
    except Exception:
        pass

def check_history_reset():
    """Reset history jika hari sudah berganti (00:00 WIB)"""
    current_date = datetime.now(WIB).date()
    if history_state["date"] != current_date:
        history_state["data"].clear()
        history_state["date"] = current_date

# ── Core Commands ──────────────────────────────────────────────────────────────
@app.on_message(filters.command(["all", "tagall"], prefixes=["/", "!"]) & filters.group)
async def tag_all_users(_, message: Message):
    if not message.from_user:
        return
        
    chat_id = message.chat.id

    if not await is_admin(chat_id, message.from_user.id):
        sent = await message.reply_text("🔒 Hanya admin yang bisa menggunakan command ini.")
        asyncio.create_task(_auto_delete(sent))
        return

    # Cancel task lama jika masih berjalan
    if chat_id in TASKS:
        TASKS[chat_id].cancel()

    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        sent = await message.reply_text("ℹ️ Penggunaan: <code>/tagall Halo semua!</code> atau balas sebuah pesan.")
        asyncio.create_task(_auto_delete(sent))
        return

    text = clean_text(message.text.split(None, 1)[1]) if len(message.command) > 1 else None
    progress = await message.reply_text("⏳ <b>Mencari member grup...</b>")

    # Inisialisasi ID pesan untuk grup ini
    if chat_id not in MSG_IDS_TO_DELETE:
        MSG_IDS_TO_DELETE[chat_id] = []

    async def run_tag():
        total_tagged = 0
        sent_ids = []
        first_msg_link = None
        
        try:
            members = [m async for m in app.get_chat_members(chat_id)]
            await progress.edit_text(f"⏳ <b>Memulai tag untuk {len(members)} member...</b>")
            
            usertxt = ""
            emoji_seq = random.choice(EMOJI)
            emoji_idx = 0
            batch_count = 0
            
            markup = InlineKeyboardMarkup([[InlineKeyboardButton("🚫 Berhentikan", callback_data=f"stop:{chat_id}", style=ButtonStyle.DANGER, icon_custom_emoji_id="5427009714745517609")]]
            )

            async def _flush(batch_text: str):
                nonlocal first_msg_link
                msg_text = f"{text}\n\n{batch_text}" if text else batch_text
                
                # Kirim batch dengan tombol STOP
                sent_msg = await app.send_message(
                    chat_id, msg_text, reply_to_message_id=replied.id if replied else None,
                    disable_web_page_preview=True, parse_mode=ParseMode.HTML, reply_markup=markup
                )
                sent_ids.append(sent_msg.id)
                MSG_IDS_TO_DELETE[chat_id].append(sent_msg.id)
                
                # Simpan link pesan pertama untuk history
                if not first_msg_link and sent_msg.link:
                    first_msg_link = sent_msg.link
                    
                await asyncio.sleep(SLEEP_BETWEEN)

            for member in members:
                if not member.user or member.user.is_deleted or member.user.is_bot:
                    continue

                emoji = emoji_seq[emoji_idx % len(emoji_seq)]
                tag = f'<a href="tg://user?id={member.user.id}">{emoji}</a> '
                emoji_idx += 1
                total_tagged += 1
                batch_count += 1
                usertxt += tag

                if len(usertxt) + _PER_MENTION_EST > TG_MAX_LENGTH or batch_count >= MAX_BATCH_SIZE:
                    await _flush(usertxt)
                    usertxt = ""
                    batch_count = 0
                    emoji_seq = random.choice(EMOJI)
                    emoji_idx = 0

            if usertxt:
                await _flush(usertxt)

            # Selesai: Record history & Tampilkan tombol Delete
            check_history_reset()
            if first_msg_link:
                if chat_id not in history_state["data"]:
                    history_state["data"][chat_id] = []
                
                time_str = datetime.now(WIB).strftime("%H:%M:%S")
                history_state["data"][chat_id].append({"time": time_str, "link": first_msg_link})

            btn_delete = InlineKeyboardMarkup([[InlineKeyboardButton("🗑 Hapus Semua Tagall", callback_data="delete_all", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5427009714745517609")]])
            await progress.edit_text(
                f"✅ <b>Tagging Selesai!</b>\n👥 Total member: <b>{len(members)}</b>\n🏷 Berhasil ditag: <b>{total_tagged}</b>",
                reply_markup=btn_delete
            )
            asyncio.create_task(_auto_delete(progress, 120))

        except asyncio.CancelledError:
            # Handle saat tombol STOP ditekan
            await progress.edit_text(f"🚫 <b>Tagall dihentikan.</b>\n🏷 Member ditag: <b>{total_tagged}</b>")
            asyncio.create_task(_auto_delete(progress, 30))

        except FloodWait as fw:
            await progress.edit_text(f"⚠️ <b>Flood wait {fw.value}s.</b> Proses terhenti, coba lagi nanti.")
            asyncio.create_task(_auto_delete(progress))
            
        finally:
            if TASKS.get(chat_id) == asyncio.current_task():
                TASKS.pop(chat_id, None)

    task = asyncio.create_task(run_tag())
    TASKS[chat_id] = task

# ── Callback Handlers (Buttons) ────────────────────────────────────────────────
@app.on_callback_query(filters.regex(r"^stop:(-?\d+)$"))
async def stop_btn(c, cq: CallbackQuery):
    chat_id = int(cq.data.split(":")[1])

    if not await is_admin(chat_id, cq.from_user.id):
        return await cq.answer("❌ Hanya admin yang bisa stop tagall!", show_alert=True)

    task = TASKS.get(chat_id)
    if task:
        task.cancel()
        TASKS.pop(chat_id, None)
        await cq.answer("🚫 Tagall berhasil dihentikan", show_alert=True)
        try:
            await cq.message.edit_reply_markup(reply_markup=None) # Hapus tombol stop di pesan yang diklik
        except:
            pass
    else:
        await cq.answer("⚠️ Proses tagall sudah selesai atau tidak berjalan.", show_alert=True)

@app.on_callback_query(filters.regex("delete_all"))
async def delete_all(c, cq: CallbackQuery):
    chat_id = cq.message.chat.id

    if not await is_admin(chat_id, cq.from_user.id):
        return await cq.answer("❌ Hanya admin yang bisa menghapus tagall!", show_alert=True)

    ids = MSG_IDS_TO_DELETE.get(chat_id)
    if not ids:
        return await cq.answer("⚠️ Tidak ada pesan tagall yang tersimpan.", show_alert=True)

    try:
        await cq.answer("⏳ Menghapus pesan tagall...")
        for i in range(0, len(ids), 100):
            await c.delete_messages(chat_id, ids[i:i+100])
        
        MSG_IDS_TO_DELETE.pop(chat_id, None)
        
        try:
            await cq.message.edit_text("✅ <b>Semua pesan tagall berhasil dihapus!</b>")
            asyncio.create_task(_auto_delete(cq.message, 15))
        except:
            pass
    except Exception as e:
        await cq.answer("❌ Gagal menghapus beberapa pesan", show_alert=True)

@app.on_message(filters.command(["cancel"], prefixes=["/", "!"]) & filters.group)
async def cancelcmd(_, message: Message):
    if not message.from_user:
        return
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("🔒 Hanya admin yang bisa menggunakan ini.")

    task = TASKS.get(chat_id)
    if task:
        task.cancel()
        TASKS.pop(chat_id, None)
        sent = await message.reply_text("✅ Tagging process stopped!")
    else:
        sent = await message.reply_text("ℹ️ Tidak ada tagall yang sedang berjalan.")
    asyncio.create_task(_auto_delete(sent, 15))

# ── History Command ────────────────────────────────────────────────────────────
@app.on_message(filters.command(["taghistory"], prefixes=["/", "!"]) & filters.group)
async def tag_history(_, message: Message):
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("🔒 Hanya admin yang bisa melihat history.")

    check_history_reset() # Cek apakah perlu reset sebelum menampilkan
    
    history_list = history_state["data"].get(chat_id, [])
    
    if not history_list:
        sent = await message.reply_text("📜 <b>History Tagall Hari Ini</b>\n\n<i>Belum ada tagall yang dilakukan hari ini. (Reset pukul 00:00 WIB)</i>")
        asyncio.create_task(_auto_delete(sent, 30))
        return

    text_msg = "📜 <b>History Tagall Hari Ini</b> (WIB)\n\n"
    for i, h in enumerate(history_list, 1):
        text_msg += f"{i}. ⏱ <b>{h['time']}</b> ➪ <a href='{h['link']}'>Cek Pesan</a>\n"
    
    text_msg += "\n<i>*History akan reset otomatis pada pukul 00:00 WIB.</i>"
    
    sent = await message.reply_text(text_msg, disable_web_page_preview=True)
    asyncio.create_task(_auto_delete(sent, 60))
