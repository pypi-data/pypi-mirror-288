from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SentCode = Union["raw.types.auth.SentCode", "raw.types.auth.SentCodeSuccess"]


# noinspection PyRedeclaration
class SentCode:  # type: ignore
    QUALNAME = "pyrogram.raw.base.auth.SentCode"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
