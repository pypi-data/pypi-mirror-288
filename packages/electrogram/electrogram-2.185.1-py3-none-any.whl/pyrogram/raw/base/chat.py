from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Chat = Union["raw.types.Channel", "raw.types.ChannelForbidden", "raw.types.Chat", "raw.types.ChatEmpty", "raw.types.ChatForbidden"]


# noinspection PyRedeclaration
class Chat:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Chat"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
