from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

EmojiStatus = Union["raw.types.EmojiStatus", "raw.types.EmojiStatusEmpty", "raw.types.EmojiStatusUntil"]


# noinspection PyRedeclaration
class EmojiStatus:  # type: ignore
    QUALNAME = "pyrogram.raw.base.EmojiStatus"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
