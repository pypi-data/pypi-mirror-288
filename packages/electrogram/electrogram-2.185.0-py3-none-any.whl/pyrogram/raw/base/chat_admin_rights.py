from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChatAdminRights = Union["raw.types.ChatAdminRights"]


# noinspection PyRedeclaration
class ChatAdminRights:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ChatAdminRights"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
