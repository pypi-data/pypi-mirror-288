from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChatInvite = Union["raw.types.ChatInvite", "raw.types.ChatInviteAlready", "raw.types.ChatInvitePeek"]


# noinspection PyRedeclaration
class ChatInvite:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ChatInvite"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
