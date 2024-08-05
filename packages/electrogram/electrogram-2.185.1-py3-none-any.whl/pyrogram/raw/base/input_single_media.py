from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputSingleMedia = Union["raw.types.InputSingleMedia"]


# noinspection PyRedeclaration
class InputSingleMedia:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputSingleMedia"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
