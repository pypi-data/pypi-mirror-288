from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SavedDialog = Union["raw.types.SavedDialog"]


# noinspection PyRedeclaration
class SavedDialog:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SavedDialog"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
