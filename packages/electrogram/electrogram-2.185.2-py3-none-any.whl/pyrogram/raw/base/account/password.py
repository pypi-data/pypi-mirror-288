from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Password = Union["raw.types.account.Password"]


# noinspection PyRedeclaration
class Password:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.Password"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
