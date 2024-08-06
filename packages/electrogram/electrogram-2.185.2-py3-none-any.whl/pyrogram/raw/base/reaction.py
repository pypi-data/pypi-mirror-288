from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Reaction = Union["raw.types.ReactionCustomEmoji", "raw.types.ReactionEmoji", "raw.types.ReactionEmpty"]


# noinspection PyRedeclaration
class Reaction:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Reaction"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
