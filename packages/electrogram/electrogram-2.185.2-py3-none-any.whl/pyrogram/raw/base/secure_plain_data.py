from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SecurePlainData = Union["raw.types.SecurePlainEmail", "raw.types.SecurePlainPhone"]


# noinspection PyRedeclaration
class SecurePlainData:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SecurePlainData"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
