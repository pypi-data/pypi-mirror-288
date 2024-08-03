from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BroadcastRevenueBalances = Union["raw.types.BroadcastRevenueBalances"]


# noinspection PyRedeclaration
class BroadcastRevenueBalances:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BroadcastRevenueBalances"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
