from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BotResults = Union["raw.types.messages.BotResults"]


# noinspection PyRedeclaration
class BotResults:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.BotResults"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
