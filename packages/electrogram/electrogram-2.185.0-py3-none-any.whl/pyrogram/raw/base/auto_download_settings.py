from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AutoDownloadSettings = Union["raw.types.AutoDownloadSettings"]


# noinspection PyRedeclaration
class AutoDownloadSettings:  # type: ignore
    QUALNAME = "pyrogram.raw.base.AutoDownloadSettings"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
