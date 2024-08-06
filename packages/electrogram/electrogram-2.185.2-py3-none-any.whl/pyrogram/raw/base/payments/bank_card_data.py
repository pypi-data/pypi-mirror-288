from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BankCardData = Union["raw.types.payments.BankCardData"]


# noinspection PyRedeclaration
class BankCardData:  # type: ignore
    QUALNAME = "pyrogram.raw.base.payments.BankCardData"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
