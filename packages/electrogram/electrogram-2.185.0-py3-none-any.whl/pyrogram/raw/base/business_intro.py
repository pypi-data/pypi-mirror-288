from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BusinessIntro = Union["raw.types.BusinessIntro"]


# noinspection PyRedeclaration
class BusinessIntro:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BusinessIntro"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
