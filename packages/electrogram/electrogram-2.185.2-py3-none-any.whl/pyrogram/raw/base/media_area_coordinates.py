from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MediaAreaCoordinates = Union["raw.types.MediaAreaCoordinates"]


# noinspection PyRedeclaration
class MediaAreaCoordinates:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MediaAreaCoordinates"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
