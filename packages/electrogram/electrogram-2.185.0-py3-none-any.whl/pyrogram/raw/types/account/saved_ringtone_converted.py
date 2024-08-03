from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SavedRingtoneConverted(TLObject):  # type: ignore
    __slots__: List[str] = ["document"]

    ID = 0x1f307eb7
    QUALNAME = "types.account.SavedRingtoneConverted"

    def __init__(self, *, document: "raw.base.Document") -> None:
        self.document = document  # Document

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SavedRingtoneConverted":
        # No flags
        
        document = TLObject.read(b)
        
        return SavedRingtoneConverted(document=document)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.document.write())
        
        return b.getvalue()
