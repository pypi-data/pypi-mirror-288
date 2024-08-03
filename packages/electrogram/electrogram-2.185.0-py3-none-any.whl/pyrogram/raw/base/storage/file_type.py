from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

FileType = Union["raw.types.storage.FileGif", "raw.types.storage.FileJpeg", "raw.types.storage.FileMov", "raw.types.storage.FileMp3", "raw.types.storage.FileMp4", "raw.types.storage.FilePartial", "raw.types.storage.FilePdf", "raw.types.storage.FilePng", "raw.types.storage.FileUnknown", "raw.types.storage.FileWebp"]


# noinspection PyRedeclaration
class FileType:  # type: ignore
    QUALNAME = "pyrogram.raw.base.storage.FileType"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
