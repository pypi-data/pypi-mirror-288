from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BoostsList = Union["raw.types.premium.BoostsList"]


# noinspection PyRedeclaration
class BoostsList:  # type: ignore
    QUALNAME = "pyrogram.raw.base.premium.BoostsList"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
