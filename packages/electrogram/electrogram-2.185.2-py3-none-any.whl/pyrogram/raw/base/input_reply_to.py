from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputReplyTo = Union["raw.types.InputReplyToMessage", "raw.types.InputReplyToStory"]


# noinspection PyRedeclaration
class InputReplyTo:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputReplyTo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
