from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Dialogs = Union["raw.types.messages.Dialogs", "raw.types.messages.DialogsNotModified", "raw.types.messages.DialogsSlice"]


# noinspection PyRedeclaration
class Dialogs:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.Dialogs"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
