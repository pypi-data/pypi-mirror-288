from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Config = Union["raw.types.Config"]


# noinspection PyRedeclaration
class Config:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Config"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
