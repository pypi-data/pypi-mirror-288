from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PaymentCharge = Union["raw.types.PaymentCharge"]


# noinspection PyRedeclaration
class PaymentCharge:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PaymentCharge"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
