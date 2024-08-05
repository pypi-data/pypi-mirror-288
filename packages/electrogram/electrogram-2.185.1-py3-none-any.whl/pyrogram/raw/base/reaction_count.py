from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ReactionCount = Union["raw.types.ReactionCount"]


# noinspection PyRedeclaration
class ReactionCount:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ReactionCount"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
