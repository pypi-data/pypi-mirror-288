from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SecureData = Union["raw.types.SecureData"]


# noinspection PyRedeclaration
class SecureData:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SecureData"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
