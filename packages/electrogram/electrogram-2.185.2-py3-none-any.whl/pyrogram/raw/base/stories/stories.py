from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Stories = Union["raw.types.stories.Stories"]


# noinspection PyRedeclaration
class Stories:  # type: ignore
    QUALNAME = "pyrogram.raw.base.stories.Stories"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
