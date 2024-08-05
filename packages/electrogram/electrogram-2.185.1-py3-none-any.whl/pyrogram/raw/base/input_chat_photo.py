from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputChatPhoto = Union["raw.types.InputChatPhoto", "raw.types.InputChatPhotoEmpty", "raw.types.InputChatUploadedPhoto"]


# noinspection PyRedeclaration
class InputChatPhoto:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputChatPhoto"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
