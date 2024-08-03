from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BindAuthKeyInner = Union["raw.types.BindAuthKeyInner"]


# noinspection PyRedeclaration
class BindAuthKeyInner:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BindAuthKeyInner"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
