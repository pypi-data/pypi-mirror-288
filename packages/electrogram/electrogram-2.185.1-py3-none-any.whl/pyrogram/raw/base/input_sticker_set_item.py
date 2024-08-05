from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputStickerSetItem = Union["raw.types.InputStickerSetItem"]


# noinspection PyRedeclaration
class InputStickerSetItem:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputStickerSetItem"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
