from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChatlistInvite = Union["raw.types.chatlists.ChatlistInvite", "raw.types.chatlists.ChatlistInviteAlready"]


# noinspection PyRedeclaration
class ChatlistInvite:  # type: ignore
    QUALNAME = "pyrogram.raw.base.chatlists.ChatlistInvite"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
