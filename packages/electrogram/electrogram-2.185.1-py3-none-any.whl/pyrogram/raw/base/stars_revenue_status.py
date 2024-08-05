from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StarsRevenueStatus = Union["raw.types.StarsRevenueStatus"]


# noinspection PyRedeclaration
class StarsRevenueStatus:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StarsRevenueStatus"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
