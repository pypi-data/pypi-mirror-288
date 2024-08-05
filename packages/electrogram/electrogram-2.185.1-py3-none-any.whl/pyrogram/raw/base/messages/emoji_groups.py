from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

EmojiGroups = Union["raw.types.messages.EmojiGroups", "raw.types.messages.EmojiGroupsNotModified"]


# noinspection PyRedeclaration
class EmojiGroups:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.EmojiGroups"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
