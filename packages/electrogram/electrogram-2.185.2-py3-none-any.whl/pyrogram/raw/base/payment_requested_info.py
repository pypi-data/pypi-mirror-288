from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PaymentRequestedInfo = Union["raw.types.PaymentRequestedInfo"]


# noinspection PyRedeclaration
class PaymentRequestedInfo:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PaymentRequestedInfo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
