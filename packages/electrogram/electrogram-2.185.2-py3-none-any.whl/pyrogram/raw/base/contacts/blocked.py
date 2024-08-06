from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Blocked = Union["raw.types.contacts.Blocked", "raw.types.contacts.BlockedSlice"]


# noinspection PyRedeclaration
class Blocked:  # type: ignore
    QUALNAME = "pyrogram.raw.base.contacts.Blocked"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
