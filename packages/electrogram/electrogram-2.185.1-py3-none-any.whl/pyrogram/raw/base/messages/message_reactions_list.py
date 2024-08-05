from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MessageReactionsList = Union["raw.types.messages.MessageReactionsList"]


# noinspection PyRedeclaration
class MessageReactionsList:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.MessageReactionsList"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
