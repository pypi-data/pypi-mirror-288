from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PollResults = Union["raw.types.PollResults"]


# noinspection PyRedeclaration
class PollResults:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PollResults"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
