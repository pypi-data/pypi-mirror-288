from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PageListOrderedItem = Union["raw.types.PageListOrderedItemBlocks", "raw.types.PageListOrderedItemText"]


# noinspection PyRedeclaration
class PageListOrderedItem:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PageListOrderedItem"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
