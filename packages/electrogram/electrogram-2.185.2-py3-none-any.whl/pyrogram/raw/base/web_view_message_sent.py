from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

WebViewMessageSent = Union["raw.types.WebViewMessageSent"]


# noinspection PyRedeclaration
class WebViewMessageSent:  # type: ignore
    QUALNAME = "pyrogram.raw.base.WebViewMessageSent"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
