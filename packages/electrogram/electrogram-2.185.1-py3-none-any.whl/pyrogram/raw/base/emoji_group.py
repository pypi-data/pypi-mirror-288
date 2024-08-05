from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

EmojiGroup = Union["raw.types.EmojiGroup", "raw.types.EmojiGroupGreeting", "raw.types.EmojiGroupPremium"]


# noinspection PyRedeclaration
class EmojiGroup:  # type: ignore
    QUALNAME = "pyrogram.raw.base.EmojiGroup"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
