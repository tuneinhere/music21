from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle

def stats_buttons(_, status):
    not_sudo = [
        InlineKeyboardButton(
            text=_["SA_B_1"],
            callback_data="TopOverall",
            style=ButtonStyle.PRIMARY, 
            icon_custom_emoji_id="4956214478002717877"
        )
    ]
    sudo = [
        InlineKeyboardButton(
            text=_["SA_B_2"],
            callback_data="bot_stats_sudo",
            style=ButtonStyle.PRIMARY,
            icon_custom_emoji_id="4956552088201986883"
        ),
        InlineKeyboardButton(
            text=_["SA_B_3"],
            callback_data="TopOverall",
            style=ButtonStyle.PRIMARY,
            icon_custom_emoji_id="4956214478002717877"
        ),
    ]
    upl = InlineKeyboardMarkup(
        [
            sudo if status else not_sudo,
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                    style=ButtonStyle.DANGER,
                    icon_custom_emoji_id="5323451799766582382"
                ),
            ],
        ]
    )
    return upl

def back_stats_buttons(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="stats_back",
                    style=ButtonStyle.SUCCESS,
                    icon_custom_emoji_id="5321532361702127913"
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                    style=ButtonStyle.DANGER,
                    icon_custom_emoji_id="5323451799766582382"
                ),
            ],
        ]
    )
    return upl
