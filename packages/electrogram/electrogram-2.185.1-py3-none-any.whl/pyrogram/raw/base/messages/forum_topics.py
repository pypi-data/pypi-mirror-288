from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ForumTopics = Union["raw.types.messages.ForumTopics"]


# noinspection PyRedeclaration
class ForumTopics:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.ForumTopics"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
