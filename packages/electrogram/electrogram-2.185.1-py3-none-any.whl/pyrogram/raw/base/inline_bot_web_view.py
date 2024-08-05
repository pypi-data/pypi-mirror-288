from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InlineBotWebView = Union["raw.types.InlineBotWebView"]


# noinspection PyRedeclaration
class InlineBotWebView:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InlineBotWebView"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
