from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Difference = Union["raw.types.updates.Difference", "raw.types.updates.DifferenceEmpty", "raw.types.updates.DifferenceSlice", "raw.types.updates.DifferenceTooLong"]


# noinspection PyRedeclaration
class Difference:  # type: ignore
    QUALNAME = "pyrogram.raw.base.updates.Difference"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
