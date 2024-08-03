from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SecureCredentialsEncrypted = Union["raw.types.SecureCredentialsEncrypted"]


# noinspection PyRedeclaration
class SecureCredentialsEncrypted:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SecureCredentialsEncrypted"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
