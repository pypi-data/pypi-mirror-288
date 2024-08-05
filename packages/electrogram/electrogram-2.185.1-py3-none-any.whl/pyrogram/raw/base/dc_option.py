from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

DcOption = Union["raw.types.DcOption"]


# noinspection PyRedeclaration
class DcOption:  # type: ignore
    QUALNAME = "pyrogram.raw.base.DcOption"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
