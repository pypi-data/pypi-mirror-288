from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MyBoosts = Union["raw.types.premium.MyBoosts"]


# noinspection PyRedeclaration
class MyBoosts:  # type: ignore
    QUALNAME = "pyrogram.raw.base.premium.MyBoosts"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
