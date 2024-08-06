from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SecureFile = Union["raw.types.SecureFile", "raw.types.SecureFileEmpty"]


# noinspection PyRedeclaration
class SecureFile:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SecureFile"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
