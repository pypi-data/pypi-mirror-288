from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

CollectibleInfo = Union["raw.types.fragment.CollectibleInfo"]


# noinspection PyRedeclaration
class CollectibleInfo:  # type: ignore
    QUALNAME = "pyrogram.raw.base.fragment.CollectibleInfo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
