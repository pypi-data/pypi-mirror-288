from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Poll = Union["raw.types.Poll"]


# noinspection PyRedeclaration
class Poll:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Poll"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
