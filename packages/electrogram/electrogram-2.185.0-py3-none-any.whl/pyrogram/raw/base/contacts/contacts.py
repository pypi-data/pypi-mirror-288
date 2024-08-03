from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Contacts = Union["raw.types.contacts.Contacts", "raw.types.contacts.ContactsNotModified"]


# noinspection PyRedeclaration
class Contacts:  # type: ignore
    QUALNAME = "pyrogram.raw.base.contacts.Contacts"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
