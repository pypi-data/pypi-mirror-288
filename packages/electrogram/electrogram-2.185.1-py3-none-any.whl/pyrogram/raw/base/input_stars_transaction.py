from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputStarsTransaction = Union["raw.types.InputStarsTransaction"]


# noinspection PyRedeclaration
class InputStarsTransaction:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputStarsTransaction"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
