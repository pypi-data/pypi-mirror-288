from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ContentSettings = Union["raw.types.account.ContentSettings"]


# noinspection PyRedeclaration
class ContentSettings:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.ContentSettings"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
