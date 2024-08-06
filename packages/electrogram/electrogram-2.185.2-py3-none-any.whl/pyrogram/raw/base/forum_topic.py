from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ForumTopic = Union["raw.types.ForumTopic", "raw.types.ForumTopicDeleted"]


# noinspection PyRedeclaration
class ForumTopic:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ForumTopic"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
