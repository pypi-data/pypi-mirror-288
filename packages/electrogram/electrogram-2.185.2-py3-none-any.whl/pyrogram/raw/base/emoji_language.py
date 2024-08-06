from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

EmojiLanguage = Union["raw.types.EmojiLanguage"]


# noinspection PyRedeclaration
class EmojiLanguage:  # type: ignore
    QUALNAME = "pyrogram.raw.base.EmojiLanguage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
