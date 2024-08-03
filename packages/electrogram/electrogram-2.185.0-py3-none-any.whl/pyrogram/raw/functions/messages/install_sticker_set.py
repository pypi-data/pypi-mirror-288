from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class InstallStickerSet(TLObject):  # type: ignore
    __slots__: List[str] = ["stickerset", "archived"]

    ID = 0xc78fe460
    QUALNAME = "functions.messages.InstallStickerSet"

    def __init__(self, *, stickerset: "raw.base.InputStickerSet", archived: bool) -> None:
        self.stickerset = stickerset  # InputStickerSet
        self.archived = archived  # Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InstallStickerSet":
        # No flags
        
        stickerset = TLObject.read(b)
        
        archived = Bool.read(b)
        
        return InstallStickerSet(stickerset=stickerset, archived=archived)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.stickerset.write())
        
        b.write(Bool(self.archived))
        
        return b.getvalue()
