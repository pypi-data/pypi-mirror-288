from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputEncryptedFile = Union["raw.types.InputEncryptedFile", "raw.types.InputEncryptedFileBigUploaded", "raw.types.InputEncryptedFileEmpty", "raw.types.InputEncryptedFileUploaded"]


# noinspection PyRedeclaration
class InputEncryptedFile:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputEncryptedFile"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
