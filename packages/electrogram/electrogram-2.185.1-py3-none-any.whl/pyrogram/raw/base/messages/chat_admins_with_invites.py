from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChatAdminsWithInvites = Union["raw.types.messages.ChatAdminsWithInvites"]


# noinspection PyRedeclaration
class ChatAdminsWithInvites:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.ChatAdminsWithInvites"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
