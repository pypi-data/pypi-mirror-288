from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputWebDocument = Union["raw.types.InputWebDocument"]


# noinspection PyRedeclaration
class InputWebDocument:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputWebDocument"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
