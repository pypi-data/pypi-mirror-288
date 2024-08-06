from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

EmojiList = Union["raw.types.EmojiList", "raw.types.EmojiListNotModified"]


# noinspection PyRedeclaration
class EmojiList:  # type: ignore
    QUALNAME = "pyrogram.raw.base.EmojiList"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
