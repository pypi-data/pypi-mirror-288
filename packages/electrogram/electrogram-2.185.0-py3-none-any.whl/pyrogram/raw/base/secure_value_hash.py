from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SecureValueHash = Union["raw.types.SecureValueHash"]


# noinspection PyRedeclaration
class SecureValueHash:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SecureValueHash"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
