from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputContact = Union["raw.types.InputPhoneContact"]


# noinspection PyRedeclaration
class InputContact:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputContact"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
