from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PaymentResult = Union["raw.types.payments.PaymentResult", "raw.types.payments.PaymentVerificationNeeded"]


# noinspection PyRedeclaration
class PaymentResult:  # type: ignore
    QUALNAME = "pyrogram.raw.base.payments.PaymentResult"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
