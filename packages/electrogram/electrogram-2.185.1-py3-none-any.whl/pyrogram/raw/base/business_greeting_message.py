from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BusinessGreetingMessage = Union["raw.types.BusinessGreetingMessage"]


# noinspection PyRedeclaration
class BusinessGreetingMessage:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BusinessGreetingMessage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
