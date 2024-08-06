from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputBusinessRecipients = Union["raw.types.InputBusinessRecipients"]


# noinspection PyRedeclaration
class InputBusinessRecipients:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputBusinessRecipients"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
