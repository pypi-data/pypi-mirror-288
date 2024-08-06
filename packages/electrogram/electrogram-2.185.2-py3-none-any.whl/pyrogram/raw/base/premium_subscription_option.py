from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PremiumSubscriptionOption = Union["raw.types.PremiumSubscriptionOption"]


# noinspection PyRedeclaration
class PremiumSubscriptionOption:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PremiumSubscriptionOption"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
