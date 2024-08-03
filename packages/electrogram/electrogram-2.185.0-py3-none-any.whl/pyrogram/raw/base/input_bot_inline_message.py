from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputBotInlineMessage = Union["raw.types.InputBotInlineMessageGame", "raw.types.InputBotInlineMessageMediaAuto", "raw.types.InputBotInlineMessageMediaContact", "raw.types.InputBotInlineMessageMediaGeo", "raw.types.InputBotInlineMessageMediaInvoice", "raw.types.InputBotInlineMessageMediaVenue", "raw.types.InputBotInlineMessageMediaWebPage", "raw.types.InputBotInlineMessageText"]


# noinspection PyRedeclaration
class InputBotInlineMessage:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputBotInlineMessage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
