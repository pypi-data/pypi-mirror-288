from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PasswordKdfAlgo = Union["raw.types.PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow", "raw.types.PasswordKdfAlgoUnknown"]


# noinspection PyRedeclaration
class PasswordKdfAlgo:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PasswordKdfAlgo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
