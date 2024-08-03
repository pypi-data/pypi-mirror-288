from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PageTableCell = Union["raw.types.PageTableCell"]


# noinspection PyRedeclaration
class PageTableCell:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PageTableCell"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
