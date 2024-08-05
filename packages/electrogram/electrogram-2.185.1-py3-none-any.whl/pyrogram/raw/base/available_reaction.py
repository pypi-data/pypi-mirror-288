from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AvailableReaction = Union["raw.types.AvailableReaction"]


# noinspection PyRedeclaration
class AvailableReaction:  # type: ignore
    QUALNAME = "pyrogram.raw.base.AvailableReaction"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
