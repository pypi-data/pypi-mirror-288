from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

EncryptedChat = Union["raw.types.EncryptedChat", "raw.types.EncryptedChatDiscarded", "raw.types.EncryptedChatEmpty", "raw.types.EncryptedChatRequested", "raw.types.EncryptedChatWaiting"]


# noinspection PyRedeclaration
class EncryptedChat:  # type: ignore
    QUALNAME = "pyrogram.raw.base.EncryptedChat"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
