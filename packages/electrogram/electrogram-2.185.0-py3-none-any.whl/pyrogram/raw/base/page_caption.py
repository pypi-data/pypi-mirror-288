from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PageCaption = Union["raw.types.PageCaption"]


# noinspection PyRedeclaration
class PageCaption:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PageCaption"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
