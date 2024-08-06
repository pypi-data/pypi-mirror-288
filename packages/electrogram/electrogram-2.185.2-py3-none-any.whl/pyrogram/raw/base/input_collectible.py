from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputCollectible = Union["raw.types.InputCollectiblePhone", "raw.types.InputCollectibleUsername"]


# noinspection PyRedeclaration
class InputCollectible:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputCollectible"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
