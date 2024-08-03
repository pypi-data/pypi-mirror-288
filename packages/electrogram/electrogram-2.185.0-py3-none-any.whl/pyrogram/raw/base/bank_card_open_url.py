from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BankCardOpenUrl = Union["raw.types.BankCardOpenUrl"]


# noinspection PyRedeclaration
class BankCardOpenUrl:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BankCardOpenUrl"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
