from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

GiveawayInfo = Union["raw.types.payments.GiveawayInfo", "raw.types.payments.GiveawayInfoResults"]


# noinspection PyRedeclaration
class GiveawayInfo:  # type: ignore
    QUALNAME = "pyrogram.raw.base.payments.GiveawayInfo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
