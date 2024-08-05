from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AffectedFoundMessages = Union["raw.types.messages.AffectedFoundMessages"]


# noinspection PyRedeclaration
class AffectedFoundMessages:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.AffectedFoundMessages"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
