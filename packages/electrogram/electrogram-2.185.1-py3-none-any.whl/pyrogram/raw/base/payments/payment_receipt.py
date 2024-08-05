from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PaymentReceipt = Union["raw.types.payments.PaymentReceipt", "raw.types.payments.PaymentReceiptStars"]


# noinspection PyRedeclaration
class PaymentReceipt:  # type: ignore
    QUALNAME = "pyrogram.raw.base.payments.PaymentReceipt"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
