from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

KeyboardButton = Union["raw.types.InputKeyboardButtonRequestPeer", "raw.types.InputKeyboardButtonUrlAuth", "raw.types.InputKeyboardButtonUserProfile", "raw.types.KeyboardButton", "raw.types.KeyboardButtonBuy", "raw.types.KeyboardButtonCallback", "raw.types.KeyboardButtonGame", "raw.types.KeyboardButtonRequestGeoLocation", "raw.types.KeyboardButtonRequestPeer", "raw.types.KeyboardButtonRequestPhone", "raw.types.KeyboardButtonRequestPoll", "raw.types.KeyboardButtonSimpleWebView", "raw.types.KeyboardButtonSwitchInline", "raw.types.KeyboardButtonUrl", "raw.types.KeyboardButtonUrlAuth", "raw.types.KeyboardButtonUserProfile", "raw.types.KeyboardButtonWebView"]


# noinspection PyRedeclaration
class KeyboardButton:  # type: ignore
    QUALNAME = "pyrogram.raw.base.KeyboardButton"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
