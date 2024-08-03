from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ExportedChatInvite = Union["raw.types.ChatInviteExported", "raw.types.ChatInvitePublicJoinRequests"]


# noinspection PyRedeclaration
class ExportedChatInvite:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ExportedChatInvite"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
