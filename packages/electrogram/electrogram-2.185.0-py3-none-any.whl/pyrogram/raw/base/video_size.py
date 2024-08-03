from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

VideoSize = Union["raw.types.VideoSize", "raw.types.VideoSizeEmojiMarkup", "raw.types.VideoSizeStickerMarkup"]


# noinspection PyRedeclaration
class VideoSize:  # type: ignore
    QUALNAME = "pyrogram.raw.base.VideoSize"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
