from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

WebPage = Union["raw.types.WebPage", "raw.types.WebPageEmpty", "raw.types.WebPageNotModified", "raw.types.WebPagePending"]


# noinspection PyRedeclaration
class WebPage:  # type: ignore
    QUALNAME = "pyrogram.raw.base.WebPage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
