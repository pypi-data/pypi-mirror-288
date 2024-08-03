from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChatAdminWithInvites = Union["raw.types.ChatAdminWithInvites"]


# noinspection PyRedeclaration
class ChatAdminWithInvites:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ChatAdminWithInvites"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
