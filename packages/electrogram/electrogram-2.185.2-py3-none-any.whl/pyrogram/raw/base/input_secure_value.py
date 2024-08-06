from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputSecureValue = Union["raw.types.InputSecureValue"]


# noinspection PyRedeclaration
class InputSecureValue:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputSecureValue"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
