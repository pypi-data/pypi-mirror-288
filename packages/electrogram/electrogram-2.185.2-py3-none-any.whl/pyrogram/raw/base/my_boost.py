from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MyBoost = Union["raw.types.MyBoost"]


# noinspection PyRedeclaration
class MyBoost:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MyBoost"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
