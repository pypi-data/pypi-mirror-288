from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

JSONObjectValue = Union["raw.types.JsonObjectValue"]


# noinspection PyRedeclaration
class JSONObjectValue:  # type: ignore
    QUALNAME = "pyrogram.raw.base.JSONObjectValue"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
