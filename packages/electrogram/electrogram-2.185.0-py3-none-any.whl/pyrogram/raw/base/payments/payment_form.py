from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PaymentForm = Union["raw.types.payments.PaymentForm", "raw.types.payments.PaymentFormStars"]


# noinspection PyRedeclaration
class PaymentForm:  # type: ignore
    QUALNAME = "pyrogram.raw.base.payments.PaymentForm"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
