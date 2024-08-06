from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SponsoredMessages = Union["raw.types.messages.SponsoredMessages", "raw.types.messages.SponsoredMessagesEmpty"]


# noinspection PyRedeclaration
class SponsoredMessages:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.SponsoredMessages"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
