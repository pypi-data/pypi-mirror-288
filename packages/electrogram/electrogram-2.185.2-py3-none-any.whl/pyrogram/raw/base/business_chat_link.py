from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BusinessChatLink = Union["raw.types.BusinessChatLink"]


# noinspection PyRedeclaration
class BusinessChatLink:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BusinessChatLink"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
