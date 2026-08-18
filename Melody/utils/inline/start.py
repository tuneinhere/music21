from pyrogram.types import InlineKeyboardButton
from pyrogram.enums import ButtonStyle
import config
from Melody import app

def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.PRIMARY,
                icon_custom_emoji_id="5321373065660088847"
            ),
            InlineKeyboardButton(text=_["S_B_2"], url=f"https://t.me/{config.SUPPORT_GROUP}",
                icon_custom_emoji_id="6138955270530797645")
        ],
        [
            InlineKeyboardButton(text="ᴀʙᴏᴜᴛ", callback_data="about_page",
              style=ButtonStyle.SUCCESS,
              icon_custom_emoji_id="6138810384104034730"),
        ],
    ]
    return buttons

def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.PRIMARY,
                icon_custom_emoji_id="6034916581207707551"
            )
        ],
        [
            InlineKeyboardButton(text="ᴀʙᴏᴜᴛ", callback_data="about_page"),
            InlineKeyboardButton(text="ᴏᴡɴᴇʀ", callback_data="owner_page", icon_custom_emoji_id="5445019302891638647"),
        ],
          [
            InlineKeyboardButton(text="ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="help_page_1", style=ButtonStyle.SUCCESS, icon_custom_emoji_id="5445275347366989283"),
        ],
    ]
    return buttons

def about_panel(_):
    buttons = [
        [
            InlineKeyboardButton(text="ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{config.SUPPORT_CHANNEL}"),
            InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{config.SUPPORT_GROUP}"),
        ],
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper", style=ButtonStyle.DANGER, icon_custom_emoji_id="5321532361702127913")
        ]
    ]
    return buttons

def owner_panel(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["S_B_12"], user_id=config.OWNER_ID),
            InlineKeyboardButton(text=_["S_B_5"], user_id=config.DEV_ID),
        ],
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper", style=ButtonStyle.DANGER, icon_custom_emoji_id="5321532361702127913"),
        ]
    ]
    return buttons
