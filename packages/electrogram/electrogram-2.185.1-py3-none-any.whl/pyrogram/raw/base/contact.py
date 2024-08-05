from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Contact = Union["raw.types.Contact"]


# noinspection PyRedeclaration
class Contact:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Contact"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
