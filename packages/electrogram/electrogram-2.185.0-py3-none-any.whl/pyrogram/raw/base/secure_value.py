from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SecureValue = Union["raw.types.SecureValue"]


# noinspection PyRedeclaration
class SecureValue:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SecureValue"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
