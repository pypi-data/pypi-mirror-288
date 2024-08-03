from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Found = Union["raw.types.contacts.Found"]


# noinspection PyRedeclaration
class Found:  # type: ignore
    QUALNAME = "pyrogram.raw.base.contacts.Found"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
