from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MessageReplyHeader = Union["raw.types.MessageReplyHeader", "raw.types.MessageReplyStoryHeader"]


# noinspection PyRedeclaration
class MessageReplyHeader:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MessageReplyHeader"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
