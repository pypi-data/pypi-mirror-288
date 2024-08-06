from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

EncryptedFile = Union["raw.types.EncryptedFile", "raw.types.EncryptedFileEmpty"]


# noinspection PyRedeclaration
class EncryptedFile:  # type: ignore
    QUALNAME = "pyrogram.raw.base.EncryptedFile"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
