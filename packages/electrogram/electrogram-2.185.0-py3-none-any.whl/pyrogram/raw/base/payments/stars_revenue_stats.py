from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StarsRevenueStats = Union["raw.types.payments.StarsRevenueStats"]


# noinspection PyRedeclaration
class StarsRevenueStats:  # type: ignore
    QUALNAME = "pyrogram.raw.base.payments.StarsRevenueStats"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
