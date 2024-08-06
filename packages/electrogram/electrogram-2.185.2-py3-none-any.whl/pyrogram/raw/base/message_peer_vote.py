from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MessagePeerVote = Union["raw.types.MessagePeerVote", "raw.types.MessagePeerVoteInputOption", "raw.types.MessagePeerVoteMultiple"]


# noinspection PyRedeclaration
class MessagePeerVote:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MessagePeerVote"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
