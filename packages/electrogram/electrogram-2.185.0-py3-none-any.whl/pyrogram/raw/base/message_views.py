from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MessageViews = Union["raw.types.MessageViews"]


# noinspection PyRedeclaration
class MessageViews:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MessageViews"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
