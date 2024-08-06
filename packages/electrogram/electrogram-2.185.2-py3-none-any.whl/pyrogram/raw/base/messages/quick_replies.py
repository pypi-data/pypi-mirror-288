from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

QuickReplies = Union["raw.types.messages.QuickReplies", "raw.types.messages.QuickRepliesNotModified"]


# noinspection PyRedeclaration
class QuickReplies:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.QuickReplies"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
