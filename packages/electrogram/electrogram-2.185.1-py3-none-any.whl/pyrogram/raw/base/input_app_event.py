from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputAppEvent = Union["raw.types.InputAppEvent"]


# noinspection PyRedeclaration
class InputAppEvent:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputAppEvent"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
