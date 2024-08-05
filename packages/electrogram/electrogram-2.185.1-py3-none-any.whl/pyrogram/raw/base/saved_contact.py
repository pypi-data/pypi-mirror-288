from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SavedContact = Union["raw.types.SavedPhoneContact"]


# noinspection PyRedeclaration
class SavedContact:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SavedContact"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
