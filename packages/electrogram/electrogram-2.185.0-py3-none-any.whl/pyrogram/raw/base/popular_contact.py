from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PopularContact = Union["raw.types.PopularContact"]


# noinspection PyRedeclaration
class PopularContact:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PopularContact"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
