from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputEncryptedChat = Union["raw.types.InputEncryptedChat"]


# noinspection PyRedeclaration
class InputEncryptedChat:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputEncryptedChat"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
