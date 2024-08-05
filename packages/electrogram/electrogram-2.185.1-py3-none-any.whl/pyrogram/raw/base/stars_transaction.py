from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StarsTransaction = Union["raw.types.StarsTransaction"]


# noinspection PyRedeclaration
class StarsTransaction:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StarsTransaction"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
