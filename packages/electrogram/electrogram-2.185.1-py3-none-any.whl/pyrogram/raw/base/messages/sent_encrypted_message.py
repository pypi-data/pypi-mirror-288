from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SentEncryptedMessage = Union["raw.types.messages.SentEncryptedFile", "raw.types.messages.SentEncryptedMessage"]


# noinspection PyRedeclaration
class SentEncryptedMessage:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.SentEncryptedMessage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
