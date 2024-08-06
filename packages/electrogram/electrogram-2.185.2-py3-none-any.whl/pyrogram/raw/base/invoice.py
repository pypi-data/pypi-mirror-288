from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Invoice = Union["raw.types.Invoice"]


# noinspection PyRedeclaration
class Invoice:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Invoice"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
