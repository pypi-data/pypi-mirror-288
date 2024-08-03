from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

File = Union["raw.types.upload.File", "raw.types.upload.FileCdnRedirect"]


# noinspection PyRedeclaration
class File:  # type: ignore
    QUALNAME = "pyrogram.raw.base.upload.File"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
