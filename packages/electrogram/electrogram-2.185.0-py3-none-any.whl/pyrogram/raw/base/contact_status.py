from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ContactStatus = Union["raw.types.ContactStatus"]


# noinspection PyRedeclaration
class ContactStatus:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ContactStatus"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
