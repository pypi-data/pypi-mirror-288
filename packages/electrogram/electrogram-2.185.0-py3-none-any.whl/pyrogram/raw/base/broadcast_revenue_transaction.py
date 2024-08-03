from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BroadcastRevenueTransaction = Union["raw.types.BroadcastRevenueTransactionProceeds", "raw.types.BroadcastRevenueTransactionRefund", "raw.types.BroadcastRevenueTransactionWithdrawal"]


# noinspection PyRedeclaration
class BroadcastRevenueTransaction:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BroadcastRevenueTransaction"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
