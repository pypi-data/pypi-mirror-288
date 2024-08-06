from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Authorization = Union["raw.types.Authorization"]


# noinspection PyRedeclaration
class Authorization:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Authorization"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
