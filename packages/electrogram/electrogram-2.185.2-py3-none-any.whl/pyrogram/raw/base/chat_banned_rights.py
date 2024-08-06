from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChatBannedRights = Union["raw.types.ChatBannedRights"]


# noinspection PyRedeclaration
class ChatBannedRights:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ChatBannedRights"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
