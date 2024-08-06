from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

LangPackLanguage = Union["raw.types.LangPackLanguage"]


# noinspection PyRedeclaration
class LangPackLanguage:  # type: ignore
    QUALNAME = "pyrogram.raw.base.LangPackLanguage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
