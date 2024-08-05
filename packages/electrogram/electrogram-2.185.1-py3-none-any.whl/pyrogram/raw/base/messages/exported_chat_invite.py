from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ExportedChatInvite = Union["raw.types.messages.ExportedChatInvite", "raw.types.messages.ExportedChatInviteReplaced"]


# noinspection PyRedeclaration
class ExportedChatInvite:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.ExportedChatInvite"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
