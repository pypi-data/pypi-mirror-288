from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputBusinessBotRecipients = Union["raw.types.InputBusinessBotRecipients"]


# noinspection PyRedeclaration
class InputBusinessBotRecipients:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputBusinessBotRecipients"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
