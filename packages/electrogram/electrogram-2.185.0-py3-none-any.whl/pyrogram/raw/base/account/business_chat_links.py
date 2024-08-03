from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BusinessChatLinks = Union["raw.types.account.BusinessChatLinks"]


# noinspection PyRedeclaration
class BusinessChatLinks:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.BusinessChatLinks"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
