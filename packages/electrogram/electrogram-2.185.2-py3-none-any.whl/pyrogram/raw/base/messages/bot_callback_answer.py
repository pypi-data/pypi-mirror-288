from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BotCallbackAnswer = Union["raw.types.messages.BotCallbackAnswer"]


# noinspection PyRedeclaration
class BotCallbackAnswer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.BotCallbackAnswer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
