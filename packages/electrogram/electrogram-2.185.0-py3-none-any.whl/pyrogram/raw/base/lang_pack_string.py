from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

LangPackString = Union["raw.types.LangPackString", "raw.types.LangPackStringDeleted", "raw.types.LangPackStringPluralized"]


# noinspection PyRedeclaration
class LangPackString:  # type: ignore
    QUALNAME = "pyrogram.raw.base.LangPackString"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
