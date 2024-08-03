from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MessagePeerReaction = Union["raw.types.MessagePeerReaction"]


# noinspection PyRedeclaration
class MessagePeerReaction:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MessagePeerReaction"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
