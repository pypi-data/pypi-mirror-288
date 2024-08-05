from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SavedReactionTag = Union["raw.types.SavedReactionTag"]


# noinspection PyRedeclaration
class SavedReactionTag:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SavedReactionTag"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
