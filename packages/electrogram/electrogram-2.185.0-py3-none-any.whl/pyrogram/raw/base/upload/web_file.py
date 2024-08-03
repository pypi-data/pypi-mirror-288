from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

WebFile = Union["raw.types.upload.WebFile"]


# noinspection PyRedeclaration
class WebFile:  # type: ignore
    QUALNAME = "pyrogram.raw.base.upload.WebFile"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
