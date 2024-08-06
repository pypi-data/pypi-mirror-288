from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputBotInlineMessageID = Union["raw.types.InputBotInlineMessageID", "raw.types.InputBotInlineMessageID64"]


# noinspection PyRedeclaration
class InputBotInlineMessageID:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputBotInlineMessageID"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
