from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ContactBirthdays = Union["raw.types.contacts.ContactBirthdays"]


# noinspection PyRedeclaration
class ContactBirthdays:  # type: ignore
    QUALNAME = "pyrogram.raw.base.contacts.ContactBirthdays"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
