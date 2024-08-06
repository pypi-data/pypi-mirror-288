from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SavedReactionTags = Union["raw.types.messages.SavedReactionTags", "raw.types.messages.SavedReactionTagsNotModified"]


# noinspection PyRedeclaration
class SavedReactionTags:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.SavedReactionTags"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
