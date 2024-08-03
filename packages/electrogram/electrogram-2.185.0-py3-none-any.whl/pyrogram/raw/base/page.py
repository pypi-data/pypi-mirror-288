from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Page = Union["raw.types.Page"]


# noinspection PyRedeclaration
class Page:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Page"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
