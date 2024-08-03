from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

EmojiStatuses = Union["raw.types.account.EmojiStatuses", "raw.types.account.EmojiStatusesNotModified"]


# noinspection PyRedeclaration
class EmojiStatuses:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.EmojiStatuses"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
