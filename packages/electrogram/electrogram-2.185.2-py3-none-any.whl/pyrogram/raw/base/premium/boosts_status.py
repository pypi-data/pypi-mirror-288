from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BoostsStatus = Union["raw.types.premium.BoostsStatus"]


# noinspection PyRedeclaration
class BoostsStatus:  # type: ignore
    QUALNAME = "pyrogram.raw.base.premium.BoostsStatus"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
