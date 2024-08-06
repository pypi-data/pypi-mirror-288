from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InvitedUsers = Union["raw.types.messages.InvitedUsers"]


# noinspection PyRedeclaration
class InvitedUsers:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.InvitedUsers"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
