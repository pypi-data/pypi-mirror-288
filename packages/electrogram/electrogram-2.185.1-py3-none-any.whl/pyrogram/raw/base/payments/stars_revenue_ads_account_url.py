from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StarsRevenueAdsAccountUrl = Union["raw.types.payments.StarsRevenueAdsAccountUrl"]


# noinspection PyRedeclaration
class StarsRevenueAdsAccountUrl:  # type: ignore
    QUALNAME = "pyrogram.raw.base.payments.StarsRevenueAdsAccountUrl"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
