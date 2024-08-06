from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

WebPageAttribute = Union["raw.types.WebPageAttributeStickerSet", "raw.types.WebPageAttributeStory", "raw.types.WebPageAttributeTheme"]


# noinspection PyRedeclaration
class WebPageAttribute:  # type: ignore
    QUALNAME = "pyrogram.raw.base.WebPageAttribute"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
