from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PageRelatedArticle = Union["raw.types.PageRelatedArticle"]


# noinspection PyRedeclaration
class PageRelatedArticle:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PageRelatedArticle"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
