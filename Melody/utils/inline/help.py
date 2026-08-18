"""
[Melody Music Bot]
Rebranded and Optimized.
All rights reserved.
"""

from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle
from Melody import app

def help_pannel_page1(_, START: Union[bool, int] = None):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5258011929993026890"),
                InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5260399854500191689"),
                InlineKeyboardButton(text=_["H_B_3"], callback_data="help_callback hb3", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5258084656674250503"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_4"], callback_data="help_callback hb4", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5296678515536581003"),
                InlineKeyboardButton(text=_["H_B_5"], callback_data="help_callback hb5", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5258430848218176413"),
                InlineKeyboardButton(text=_["H_B_6"], callback_data="help_callback hb6", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5258391252914676042"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_7"], callback_data="help_callback hb7", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5258278668936945760"),
                InlineKeyboardButton(text=_["H_B_8"], callback_data="help_callback hb8", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5199457120428249992"),
                InlineKeyboardButton(text=_["H_B_9"], callback_data="help_callback hb9", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5258093637450866522"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_10"], callback_data="help_callback hb10", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5321097148371058002"),
            ],
            [
                InlineKeyboardButton(text="️Back page", callback_data="help_page_3", style=ButtonStyle.SUCCESS, icon_custom_emoji_id="5321532361702127913"))
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"] if START else _["CLOSE_BUTTON"],
                    callback_data="settingsback_helper" if START else "close",
                    style=ButtonStyle.DANGER, icon_custom_emoji_id="5323451799766582382")
                ),
                InlineKeyboardButton(text="️Next page", callback_data="help_page_2", style=ButtonStyle.SUCCESS, icon_custom_emoji_id="5321300317504030049")),
            ],
        ]
    )

def help_pannel_page2(_, START: Union[bool, int] = None):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_11"], callback_data="help_callback hb11", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5359529383319084413"),
                InlineKeyboardButton(text=_["H_B_12"], callback_data="help_callback hb12", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5260687681733533075"),
                InlineKeyboardButton(text=_["H_B_13"], callback_data="help_callback hb13", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5258216851472654189"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_14"], callback_data="help_callback hb14", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5258334469152054985"),
                InlineKeyboardButton(text=_["H_B_15"], callback_data="help_callback hb15", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5204189706237004154"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_20"], callback_data="help_callback hb20", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5258513401784573443"),
            ],
            [
                InlineKeyboardButton(text="️back page", callback_data="help_page_1", style=ButtonStyle.SUCCESS, icon_custom_emoji_id="5321532361702127913"),
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"] if START else _["CLOSE_BUTTON"],
                    callback_data="settingsback_helper" if START else "close",
                    style=ButtonStyle.DANGER, icon_custom_emoji_id="5323451799766582382"
                ),
                InlineKeyboardButton(text="️next page", callback_data="help_page_3", style=ButtonStyle.SUCCESS, icon_custom_emoji_id="5321300317504030049"),
            ],
        ]
    )

def help_pannel_page3(_, START: Union[bool, int] = None):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_21"], callback_data="help_callback hb21", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5258514780469075716"),
                InlineKeyboardButton(text=_["H_B_23"], callback_data="help_callback hb23", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5260730055880876557"),
                InlineKeyboardButton(text=_["H_B_24"], callback_data="help_callback hb24", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5256143829672672750"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_29"], callback_data="help_callback hb29", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5256143829672672750"),
                InlineKeyboardButton(text=_["H_B_39"], callback_data="help_callback hb39", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5370546867786523009"),
            ],
            [
                InlineKeyboardButton(text="️Back Page", callback_data="help_page_2", style=ButtonStyle.SUCCESS, icon_custom_emoji_id="5321532361702127913"),
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"] if START else _["CLOSE_BUTTON"],
                    callback_data="settingsback_helper" if START else "close",
                    style=ButtonStyle.DANGER, icon_custom_emoji_id="5323451799766582382"
                ),
                InlineKeyboardButton(text="️Next Page", callback_data="help_page_1", style=ButtonStyle.SUCCESS, icon_custom_emoji_id="5323451799766582382"),
            ],
        ]
    )

def help_back_markup(_, page: int = 1):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"help_page_{page}",
                    style=ButtonStyle.DANGER
                )
            ]
        ]
    )

def private_help_panel(_):
    return [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{app.username}?start=help",
                style=ButtonStyle.SUCCESS
            ),
        ]
    ]
