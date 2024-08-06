from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BadMsgNotification = Union["raw.types.BadMsgNotification", "raw.types.BadServerSalt"]


# noinspection PyRedeclaration
class BadMsgNotification:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BadMsgNotification"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
