from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SecurePasswordKdfAlgo = Union["raw.types.SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000", "raw.types.SecurePasswordKdfAlgoSHA512", "raw.types.SecurePasswordKdfAlgoUnknown"]


# noinspection PyRedeclaration
class SecurePasswordKdfAlgo:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SecurePasswordKdfAlgo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
