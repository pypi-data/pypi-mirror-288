from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AvailableReactions = Union["raw.types.messages.AvailableReactions", "raw.types.messages.AvailableReactionsNotModified"]


# noinspection PyRedeclaration
class AvailableReactions:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.AvailableReactions"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
