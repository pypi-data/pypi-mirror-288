from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputWebFileLocation = Union["raw.types.InputWebFileAudioAlbumThumbLocation", "raw.types.InputWebFileGeoPointLocation", "raw.types.InputWebFileLocation"]


# noinspection PyRedeclaration
class InputWebFileLocation:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputWebFileLocation"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
