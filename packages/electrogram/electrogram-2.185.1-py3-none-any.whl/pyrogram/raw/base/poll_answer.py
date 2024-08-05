from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PollAnswer = Union["raw.types.PollAnswer"]


# noinspection PyRedeclaration
class PollAnswer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PollAnswer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
