from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SponsoredMessage = Union["raw.types.SponsoredMessage"]


# noinspection PyRedeclaration
class SponsoredMessage:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SponsoredMessage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
