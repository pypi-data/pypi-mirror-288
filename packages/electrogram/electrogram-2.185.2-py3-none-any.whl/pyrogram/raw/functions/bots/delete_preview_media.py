from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class DeletePreviewMedia(TLObject):  # type: ignore
    __slots__: List[str] = ["bot", "lang_code", "media"]

    ID = 0x2d0135b3
    QUALNAME = "functions.bots.DeletePreviewMedia"

    def __init__(self, *, bot: "raw.base.InputUser", lang_code: str, media: List["raw.base.InputMedia"]) -> None:
        self.bot = bot  # InputUser
        self.lang_code = lang_code  # string
        self.media = media  # Vector<InputMedia>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DeletePreviewMedia":
        # No flags
        
        bot = TLObject.read(b)
        
        lang_code = String.read(b)
        
        media = TLObject.read(b)
        
        return DeletePreviewMedia(bot=bot, lang_code=lang_code, media=media)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.bot.write())
        
        b.write(String(self.lang_code))
        
        b.write(Vector(self.media))
        
        return b.getvalue()
