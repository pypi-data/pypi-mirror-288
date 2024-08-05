from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MediaArea = Union["raw.types.InputMediaAreaChannelPost", "raw.types.InputMediaAreaVenue", "raw.types.MediaAreaChannelPost", "raw.types.MediaAreaGeoPoint", "raw.types.MediaAreaSuggestedReaction", "raw.types.MediaAreaUrl", "raw.types.MediaAreaVenue", "raw.types.MediaAreaWeather"]


# noinspection PyRedeclaration
class MediaArea:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MediaArea"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
