from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

DocumentAttribute = Union["raw.types.DocumentAttributeAnimated", "raw.types.DocumentAttributeAudio", "raw.types.DocumentAttributeCustomEmoji", "raw.types.DocumentAttributeFilename", "raw.types.DocumentAttributeHasStickers", "raw.types.DocumentAttributeImageSize", "raw.types.DocumentAttributeSticker", "raw.types.DocumentAttributeVideo"]


# noinspection PyRedeclaration
class DocumentAttribute:  # type: ignore
    QUALNAME = "pyrogram.raw.base.DocumentAttribute"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
