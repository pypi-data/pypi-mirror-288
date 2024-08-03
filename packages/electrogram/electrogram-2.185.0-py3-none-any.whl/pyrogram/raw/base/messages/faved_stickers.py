from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

FavedStickers = Union["raw.types.messages.FavedStickers", "raw.types.messages.FavedStickersNotModified"]


# noinspection PyRedeclaration
class FavedStickers:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.FavedStickers"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
