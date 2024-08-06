from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

FactCheck = Union["raw.types.FactCheck"]


# noinspection PyRedeclaration
class FactCheck:  # type: ignore
    QUALNAME = "pyrogram.raw.base.FactCheck"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
