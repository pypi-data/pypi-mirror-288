from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BotInlineResult = Union["raw.types.BotInlineMediaResult", "raw.types.BotInlineResult"]


# noinspection PyRedeclaration
class BotInlineResult:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BotInlineResult"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
