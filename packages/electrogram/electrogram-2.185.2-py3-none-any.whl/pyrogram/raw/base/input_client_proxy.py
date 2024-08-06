from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputClientProxy = Union["raw.types.InputClientProxy"]


# noinspection PyRedeclaration
class InputClientProxy:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputClientProxy"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
