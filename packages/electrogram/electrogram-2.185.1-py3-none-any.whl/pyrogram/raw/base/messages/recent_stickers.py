from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

RecentStickers = Union["raw.types.messages.RecentStickers", "raw.types.messages.RecentStickersNotModified"]


# noinspection PyRedeclaration
class RecentStickers:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.RecentStickers"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
