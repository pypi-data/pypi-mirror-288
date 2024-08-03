from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MessageReactions = Union["raw.types.MessageReactions"]


# noinspection PyRedeclaration
class MessageReactions:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MessageReactions"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
