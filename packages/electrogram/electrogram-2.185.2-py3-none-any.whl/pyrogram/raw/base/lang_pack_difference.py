from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

LangPackDifference = Union["raw.types.LangPackDifference"]


# noinspection PyRedeclaration
class LangPackDifference:  # type: ignore
    QUALNAME = "pyrogram.raw.base.LangPackDifference"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
