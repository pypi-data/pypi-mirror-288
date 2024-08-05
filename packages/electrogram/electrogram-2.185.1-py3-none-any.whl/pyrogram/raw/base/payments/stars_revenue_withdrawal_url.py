from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StarsRevenueWithdrawalUrl = Union["raw.types.payments.StarsRevenueWithdrawalUrl"]


# noinspection PyRedeclaration
class StarsRevenueWithdrawalUrl:  # type: ignore
    QUALNAME = "pyrogram.raw.base.payments.StarsRevenueWithdrawalUrl"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
