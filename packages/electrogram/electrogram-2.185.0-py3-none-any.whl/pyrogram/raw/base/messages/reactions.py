from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Reactions = Union["raw.types.messages.Reactions", "raw.types.messages.ReactionsNotModified"]


# noinspection PyRedeclaration
class Reactions:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.Reactions"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
