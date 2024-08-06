from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

EmojiURL = Union["raw.types.EmojiURL"]


# noinspection PyRedeclaration
class EmojiURL:  # type: ignore
    QUALNAME = "pyrogram.raw.base.EmojiURL"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
