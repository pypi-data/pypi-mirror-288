from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PaymentFormMethod = Union["raw.types.PaymentFormMethod"]


# noinspection PyRedeclaration
class PaymentFormMethod:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PaymentFormMethod"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
