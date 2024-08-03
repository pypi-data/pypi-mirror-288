from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputChatlist = Union["raw.types.InputChatlistDialogFilter"]


# noinspection PyRedeclaration
class InputChatlist:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputChatlist"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
