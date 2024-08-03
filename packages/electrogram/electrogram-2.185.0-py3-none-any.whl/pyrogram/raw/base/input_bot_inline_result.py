from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputBotInlineResult = Union["raw.types.InputBotInlineResult", "raw.types.InputBotInlineResultDocument", "raw.types.InputBotInlineResultGame", "raw.types.InputBotInlineResultPhoto"]


# noinspection PyRedeclaration
class InputBotInlineResult:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputBotInlineResult"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
