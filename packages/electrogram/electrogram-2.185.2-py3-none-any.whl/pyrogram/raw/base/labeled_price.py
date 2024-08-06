from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

LabeledPrice = Union["raw.types.LabeledPrice"]


# noinspection PyRedeclaration
class LabeledPrice:  # type: ignore
    QUALNAME = "pyrogram.raw.base.LabeledPrice"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
