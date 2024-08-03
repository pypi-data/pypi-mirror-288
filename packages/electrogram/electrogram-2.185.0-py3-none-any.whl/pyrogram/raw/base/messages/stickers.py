from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Stickers = Union["raw.types.messages.Stickers", "raw.types.messages.StickersNotModified"]


# noinspection PyRedeclaration
class Stickers:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.Stickers"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
