from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChatInviteImporter = Union["raw.types.ChatInviteImporter"]


# noinspection PyRedeclaration
class ChatInviteImporter:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ChatInviteImporter"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
