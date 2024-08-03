from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

DiscussionMessage = Union["raw.types.messages.DiscussionMessage"]


# noinspection PyRedeclaration
class DiscussionMessage:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.DiscussionMessage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
