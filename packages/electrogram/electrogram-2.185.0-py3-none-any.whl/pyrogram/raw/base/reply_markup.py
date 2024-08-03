from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ReplyMarkup = Union["raw.types.ReplyInlineMarkup", "raw.types.ReplyKeyboardForceReply", "raw.types.ReplyKeyboardHide", "raw.types.ReplyKeyboardMarkup"]


# noinspection PyRedeclaration
class ReplyMarkup:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ReplyMarkup"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
