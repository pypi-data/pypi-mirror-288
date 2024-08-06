from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BotBusinessConnection = Union["raw.types.BotBusinessConnection"]


# noinspection PyRedeclaration
class BotBusinessConnection:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BotBusinessConnection"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
