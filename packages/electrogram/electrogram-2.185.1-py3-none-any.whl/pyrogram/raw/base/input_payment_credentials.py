from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputPaymentCredentials = Union["raw.types.InputPaymentCredentials", "raw.types.InputPaymentCredentialsApplePay", "raw.types.InputPaymentCredentialsGooglePay", "raw.types.InputPaymentCredentialsSaved"]


# noinspection PyRedeclaration
class InputPaymentCredentials:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputPaymentCredentials"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
