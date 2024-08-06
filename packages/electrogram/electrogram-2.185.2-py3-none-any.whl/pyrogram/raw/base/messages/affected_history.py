from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AffectedHistory = Union["raw.types.messages.AffectedHistory"]


# noinspection PyRedeclaration
class AffectedHistory:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.AffectedHistory"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
