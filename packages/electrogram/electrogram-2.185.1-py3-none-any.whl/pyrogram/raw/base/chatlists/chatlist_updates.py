from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChatlistUpdates = Union["raw.types.chatlists.ChatlistUpdates"]


# noinspection PyRedeclaration
class ChatlistUpdates:  # type: ignore
    QUALNAME = "pyrogram.raw.base.chatlists.ChatlistUpdates"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
