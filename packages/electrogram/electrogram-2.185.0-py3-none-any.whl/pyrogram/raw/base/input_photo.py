from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputPhoto = Union["raw.types.InputPhoto", "raw.types.InputPhotoEmpty"]


# noinspection PyRedeclaration
class InputPhoto:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputPhoto"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
