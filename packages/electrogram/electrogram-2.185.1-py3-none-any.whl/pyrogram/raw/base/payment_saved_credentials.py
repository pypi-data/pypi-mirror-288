from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PaymentSavedCredentials = Union["raw.types.PaymentSavedCredentialsCard"]


# noinspection PyRedeclaration
class PaymentSavedCredentials:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PaymentSavedCredentials"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
