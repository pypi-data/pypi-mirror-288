from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetQuickReplyMessages(TLObject):  # type: ignore
    __slots__: List[str] = ["shortcut_id", "hash", "id"]

    ID = 0x94a495c3
    QUALNAME = "functions.messages.GetQuickReplyMessages"

    def __init__(self, *, shortcut_id: int, hash: int, id: Optional[List[int]] = None) -> None:
        self.shortcut_id = shortcut_id  # int
        self.hash = hash  # long
        self.id = id  # flags.0?Vector<int>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetQuickReplyMessages":
        
        flags = Int.read(b)
        
        shortcut_id = Int.read(b)
        
        id = TLObject.read(b, Int) if flags & (1 << 0) else []
        
        hash = Long.read(b)
        
        return GetQuickReplyMessages(shortcut_id=shortcut_id, hash=hash, id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.id else 0
        b.write(Int(flags))
        
        b.write(Int(self.shortcut_id))
        
        if self.id is not None:
            b.write(Vector(self.id, Int))
        
        b.write(Long(self.hash))
        
        return b.getvalue()
