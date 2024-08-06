from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BroadcastRevenueWithdrawalUrl = Union["raw.types.stats.BroadcastRevenueWithdrawalUrl"]


# noinspection PyRedeclaration
class BroadcastRevenueWithdrawalUrl:  # type: ignore
    QUALNAME = "pyrogram.raw.base.stats.BroadcastRevenueWithdrawalUrl"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
