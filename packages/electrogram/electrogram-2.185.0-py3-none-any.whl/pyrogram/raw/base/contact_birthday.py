from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ContactBirthday = Union["raw.types.ContactBirthday"]


# noinspection PyRedeclaration
class ContactBirthday:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ContactBirthday"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
