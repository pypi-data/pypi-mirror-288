from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SentEmailCode = Union["raw.types.account.SentEmailCode"]


# noinspection PyRedeclaration
class SentEmailCode:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.SentEmailCode"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
