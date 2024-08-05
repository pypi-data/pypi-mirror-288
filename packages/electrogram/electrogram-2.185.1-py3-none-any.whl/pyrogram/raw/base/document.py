from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Document = Union["raw.types.Document", "raw.types.DocumentEmpty"]


# noinspection PyRedeclaration
class Document:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Document"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
