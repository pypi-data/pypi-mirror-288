from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputCheckPasswordSRP = Union["raw.types.InputCheckPasswordEmpty", "raw.types.InputCheckPasswordSRP"]


# noinspection PyRedeclaration
class InputCheckPasswordSRP:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputCheckPasswordSRP"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
