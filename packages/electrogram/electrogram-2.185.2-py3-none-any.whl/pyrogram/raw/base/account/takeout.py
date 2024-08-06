from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Takeout = Union["raw.types.account.Takeout"]


# noinspection PyRedeclaration
class Takeout:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.Takeout"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
