from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChatReactions = Union["raw.types.ChatReactionsAll", "raw.types.ChatReactionsNone", "raw.types.ChatReactionsSome"]


# noinspection PyRedeclaration
class ChatReactions:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ChatReactions"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
