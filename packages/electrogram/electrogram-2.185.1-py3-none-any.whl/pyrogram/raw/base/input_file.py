from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputFile = Union["raw.types.InputFile", "raw.types.InputFileBig", "raw.types.InputFileStoryDocument"]


# noinspection PyRedeclaration
class InputFile:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputFile"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
