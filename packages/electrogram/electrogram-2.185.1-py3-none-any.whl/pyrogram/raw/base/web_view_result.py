from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

WebViewResult = Union["raw.types.WebViewResultUrl"]


# noinspection PyRedeclaration
class WebViewResult:  # type: ignore
    QUALNAME = "pyrogram.raw.base.WebViewResult"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
