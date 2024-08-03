from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BotInfo = Union["raw.types.bots.BotInfo"]


# noinspection PyRedeclaration
class BotInfo:  # type: ignore
    QUALNAME = "pyrogram.raw.base.bots.BotInfo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
