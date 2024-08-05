from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputGroupCall = Union["raw.types.InputGroupCall"]


# noinspection PyRedeclaration
class InputGroupCall:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputGroupCall"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
