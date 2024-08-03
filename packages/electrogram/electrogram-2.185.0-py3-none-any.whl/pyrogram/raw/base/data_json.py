from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

DataJSON = Union["raw.types.DataJSON"]


# noinspection PyRedeclaration
class DataJSON:  # type: ignore
    QUALNAME = "pyrogram.raw.base.DataJSON"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
