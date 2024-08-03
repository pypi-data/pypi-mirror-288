from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BusinessRecipients = Union["raw.types.BusinessRecipients"]


# noinspection PyRedeclaration
class BusinessRecipients:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BusinessRecipients"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
