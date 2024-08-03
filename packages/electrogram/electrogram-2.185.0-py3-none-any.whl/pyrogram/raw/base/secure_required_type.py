from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SecureRequiredType = Union["raw.types.SecureRequiredType", "raw.types.SecureRequiredTypeOneOf"]


# noinspection PyRedeclaration
class SecureRequiredType:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SecureRequiredType"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
