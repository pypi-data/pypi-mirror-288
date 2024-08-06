from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class AvailableEffects(TLObject):  # type: ignore
    __slots__: List[str] = ["hash", "effects", "documents"]

    ID = 0xbddb616e
    QUALNAME = "types.messages.AvailableEffects"

    def __init__(self, *, hash: int, effects: List["raw.base.AvailableEffect"], documents: List["raw.base.Document"]) -> None:
        self.hash = hash  # int
        self.effects = effects  # Vector<AvailableEffect>
        self.documents = documents  # Vector<Document>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AvailableEffects":
        # No flags
        
        hash = Int.read(b)
        
        effects = TLObject.read(b)
        
        documents = TLObject.read(b)
        
        return AvailableEffects(hash=hash, effects=effects, documents=documents)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.hash))
        
        b.write(Vector(self.effects))
        
        b.write(Vector(self.documents))
        
        return b.getvalue()
