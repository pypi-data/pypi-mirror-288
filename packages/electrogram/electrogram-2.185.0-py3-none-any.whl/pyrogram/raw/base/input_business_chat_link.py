from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputBusinessChatLink = Union["raw.types.InputBusinessChatLink"]


# noinspection PyRedeclaration
class InputBusinessChatLink:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputBusinessChatLink"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
