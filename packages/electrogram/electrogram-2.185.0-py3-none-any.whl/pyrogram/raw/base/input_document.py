from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputDocument = Union["raw.types.InputDocument", "raw.types.InputDocumentEmpty"]


# noinspection PyRedeclaration
class InputDocument:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputDocument"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
