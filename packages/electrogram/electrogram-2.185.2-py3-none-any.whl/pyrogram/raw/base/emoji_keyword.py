from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

EmojiKeyword = Union["raw.types.EmojiKeyword", "raw.types.EmojiKeywordDeleted"]


# noinspection PyRedeclaration
class EmojiKeyword:  # type: ignore
    QUALNAME = "pyrogram.raw.base.EmojiKeyword"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
