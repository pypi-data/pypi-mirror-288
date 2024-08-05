from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputMessage = Union["raw.types.InputMessageCallbackQuery", "raw.types.InputMessageID", "raw.types.InputMessagePinned", "raw.types.InputMessageReplyTo"]


# noinspection PyRedeclaration
class InputMessage:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputMessage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
