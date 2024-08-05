from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

CdnFile = Union["raw.types.upload.CdnFile", "raw.types.upload.CdnFileReuploadNeeded"]


# noinspection PyRedeclaration
class CdnFile:  # type: ignore
    QUALNAME = "pyrogram.raw.base.upload.CdnFile"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
