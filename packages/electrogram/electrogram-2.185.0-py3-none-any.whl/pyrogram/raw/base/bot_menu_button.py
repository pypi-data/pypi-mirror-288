from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BotMenuButton = Union["raw.types.BotMenuButton", "raw.types.BotMenuButtonCommands", "raw.types.BotMenuButtonDefault"]


# noinspection PyRedeclaration
class BotMenuButton:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BotMenuButton"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
