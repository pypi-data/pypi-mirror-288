from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AffectedMessages = Union["raw.types.messages.AffectedMessages"]


# noinspection PyRedeclaration
class AffectedMessages:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.AffectedMessages"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
