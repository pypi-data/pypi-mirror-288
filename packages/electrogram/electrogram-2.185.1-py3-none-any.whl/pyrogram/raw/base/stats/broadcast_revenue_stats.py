from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BroadcastRevenueStats = Union["raw.types.stats.BroadcastRevenueStats"]


# noinspection PyRedeclaration
class BroadcastRevenueStats:  # type: ignore
    QUALNAME = "pyrogram.raw.base.stats.BroadcastRevenueStats"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
