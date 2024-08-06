from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AccountDaysTTL = Union["raw.types.AccountDaysTTL"]


# noinspection PyRedeclaration
class AccountDaysTTL:  # type: ignore
    QUALNAME = "pyrogram.raw.base.AccountDaysTTL"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
