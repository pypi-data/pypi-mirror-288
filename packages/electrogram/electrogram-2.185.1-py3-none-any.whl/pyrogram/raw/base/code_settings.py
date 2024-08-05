from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

CodeSettings = Union["raw.types.CodeSettings"]


# noinspection PyRedeclaration
class CodeSettings:  # type: ignore
    QUALNAME = "pyrogram.raw.base.CodeSettings"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
