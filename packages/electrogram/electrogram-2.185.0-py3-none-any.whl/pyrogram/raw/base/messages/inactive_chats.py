from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InactiveChats = Union["raw.types.messages.InactiveChats"]


# noinspection PyRedeclaration
class InactiveChats:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.InactiveChats"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
