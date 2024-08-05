from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ImportedContact = Union["raw.types.ImportedContact"]


# noinspection PyRedeclaration
class ImportedContact:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ImportedContact"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
