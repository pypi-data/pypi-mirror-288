from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PostAddress = Union["raw.types.PostAddress"]


# noinspection PyRedeclaration
class PostAddress:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PostAddress"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
