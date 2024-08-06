from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Birthday = Union["raw.types.Birthday"]


# noinspection PyRedeclaration
class Birthday:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Birthday"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
