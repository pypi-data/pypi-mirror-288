from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PostInteractionCounters = Union["raw.types.PostInteractionCountersMessage", "raw.types.PostInteractionCountersStory"]


# noinspection PyRedeclaration
class PostInteractionCounters:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PostInteractionCounters"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
