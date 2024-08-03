from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MessageFwdHeader = Union["raw.types.MessageFwdHeader"]


# noinspection PyRedeclaration
class MessageFwdHeader:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MessageFwdHeader"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
