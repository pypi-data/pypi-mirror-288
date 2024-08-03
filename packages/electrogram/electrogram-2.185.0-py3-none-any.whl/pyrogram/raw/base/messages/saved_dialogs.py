from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SavedDialogs = Union["raw.types.messages.SavedDialogs", "raw.types.messages.SavedDialogsNotModified", "raw.types.messages.SavedDialogsSlice"]


# noinspection PyRedeclaration
class SavedDialogs:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.SavedDialogs"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
