from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

CdnConfig = Union["raw.types.CdnConfig"]


# noinspection PyRedeclaration
class CdnConfig:  # type: ignore
    QUALNAME = "pyrogram.raw.base.CdnConfig"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
