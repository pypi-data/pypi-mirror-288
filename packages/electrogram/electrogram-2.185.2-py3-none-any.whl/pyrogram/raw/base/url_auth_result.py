from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

UrlAuthResult = Union["raw.types.UrlAuthResultAccepted", "raw.types.UrlAuthResultDefault", "raw.types.UrlAuthResultRequest"]


# noinspection PyRedeclaration
class UrlAuthResult:  # type: ignore
    QUALNAME = "pyrogram.raw.base.UrlAuthResult"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
