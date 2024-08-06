from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BotInlineMessage = Union["raw.types.BotInlineMessageMediaAuto", "raw.types.BotInlineMessageMediaContact", "raw.types.BotInlineMessageMediaGeo", "raw.types.BotInlineMessageMediaInvoice", "raw.types.BotInlineMessageMediaVenue", "raw.types.BotInlineMessageMediaWebPage", "raw.types.BotInlineMessageText"]


# noinspection PyRedeclaration
class BotInlineMessage:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BotInlineMessage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
