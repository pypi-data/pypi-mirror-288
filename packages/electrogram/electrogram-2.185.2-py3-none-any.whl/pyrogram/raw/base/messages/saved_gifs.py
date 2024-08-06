from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SavedGifs = Union["raw.types.messages.SavedGifs", "raw.types.messages.SavedGifsNotModified"]


# noinspection PyRedeclaration
class SavedGifs:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.SavedGifs"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
