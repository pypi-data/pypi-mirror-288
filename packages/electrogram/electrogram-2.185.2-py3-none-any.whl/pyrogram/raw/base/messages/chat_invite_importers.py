from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChatInviteImporters = Union["raw.types.messages.ChatInviteImporters"]


# noinspection PyRedeclaration
class ChatInviteImporters:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.ChatInviteImporters"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
