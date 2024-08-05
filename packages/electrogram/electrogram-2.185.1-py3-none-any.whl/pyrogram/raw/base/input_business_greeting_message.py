from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputBusinessGreetingMessage = Union["raw.types.InputBusinessGreetingMessage"]


# noinspection PyRedeclaration
class InputBusinessGreetingMessage:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputBusinessGreetingMessage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
