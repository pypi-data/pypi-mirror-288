from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BusinessBotRecipients = Union["raw.types.BusinessBotRecipients"]


# noinspection PyRedeclaration
class BusinessBotRecipients:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BusinessBotRecipients"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
