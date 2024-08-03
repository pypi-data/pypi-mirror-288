from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

DestroySessionRes = Union["raw.types.DestroySessionNone", "raw.types.DestroySessionOk"]


# noinspection PyRedeclaration
class DestroySessionRes:  # type: ignore
    QUALNAME = "pyrogram.raw.base.DestroySessionRes"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
