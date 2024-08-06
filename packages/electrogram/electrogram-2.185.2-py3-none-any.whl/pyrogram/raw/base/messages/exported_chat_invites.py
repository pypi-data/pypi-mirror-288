from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ExportedChatInvites = Union["raw.types.messages.ExportedChatInvites"]


# noinspection PyRedeclaration
class ExportedChatInvites:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.ExportedChatInvites"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
