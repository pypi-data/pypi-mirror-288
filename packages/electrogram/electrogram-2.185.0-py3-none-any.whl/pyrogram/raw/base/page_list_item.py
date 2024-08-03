from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PageListItem = Union["raw.types.PageListItemBlocks", "raw.types.PageListItemText"]


# noinspection PyRedeclaration
class PageListItem:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PageListItem"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
