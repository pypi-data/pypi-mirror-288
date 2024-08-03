from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Pong = Union["raw.types.Pong"]


# noinspection PyRedeclaration
class Pong:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Pong"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
