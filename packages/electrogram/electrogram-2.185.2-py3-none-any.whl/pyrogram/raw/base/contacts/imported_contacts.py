from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ImportedContacts = Union["raw.types.contacts.ImportedContacts"]


# noinspection PyRedeclaration
class ImportedContacts:  # type: ignore
    QUALNAME = "pyrogram.raw.base.contacts.ImportedContacts"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
