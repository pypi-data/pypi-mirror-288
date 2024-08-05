from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

EmojiKeywordsDifference = Union["raw.types.EmojiKeywordsDifference"]


# noinspection PyRedeclaration
class EmojiKeywordsDifference:  # type: ignore
    QUALNAME = "pyrogram.raw.base.EmojiKeywordsDifference"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
