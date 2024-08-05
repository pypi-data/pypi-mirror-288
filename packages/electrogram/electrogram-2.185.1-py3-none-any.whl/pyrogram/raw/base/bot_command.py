from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BotCommand = Union["raw.types.BotCommand"]


# noinspection PyRedeclaration
class BotCommand:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BotCommand"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
