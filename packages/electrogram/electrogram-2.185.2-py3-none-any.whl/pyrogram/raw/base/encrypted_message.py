from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

EncryptedMessage = Union["raw.types.EncryptedMessage", "raw.types.EncryptedMessageService"]


# noinspection PyRedeclaration
class EncryptedMessage:  # type: ignore
    QUALNAME = "pyrogram.raw.base.EncryptedMessage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
