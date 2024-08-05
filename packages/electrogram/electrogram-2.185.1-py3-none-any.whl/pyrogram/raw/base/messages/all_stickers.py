from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AllStickers = Union["raw.types.messages.AllStickers", "raw.types.messages.AllStickersNotModified"]


# noinspection PyRedeclaration
class AllStickers:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.AllStickers"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
