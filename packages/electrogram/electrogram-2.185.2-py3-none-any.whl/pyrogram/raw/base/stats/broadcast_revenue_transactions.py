from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BroadcastRevenueTransactions = Union["raw.types.stats.BroadcastRevenueTransactions"]


# noinspection PyRedeclaration
class BroadcastRevenueTransactions:  # type: ignore
    QUALNAME = "pyrogram.raw.base.stats.BroadcastRevenueTransactions"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
