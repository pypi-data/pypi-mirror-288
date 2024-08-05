from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ResPQ = Union["raw.types.ResPQ"]


# noinspection PyRedeclaration
class ResPQ:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ResPQ"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
