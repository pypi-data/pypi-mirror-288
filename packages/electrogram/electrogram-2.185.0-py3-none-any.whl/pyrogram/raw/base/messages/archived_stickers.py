from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ArchivedStickers = Union["raw.types.messages.ArchivedStickers"]


# noinspection PyRedeclaration
class ArchivedStickers:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.ArchivedStickers"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
