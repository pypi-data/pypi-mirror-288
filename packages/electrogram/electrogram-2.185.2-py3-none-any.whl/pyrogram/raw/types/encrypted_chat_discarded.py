from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class EncryptedChatDiscarded(TLObject):  # type: ignore
    __slots__: List[str] = ["id", "history_deleted"]

    ID = 0x1e1c7c45
    QUALNAME = "types.EncryptedChatDiscarded"

    def __init__(self, *, id: int, history_deleted: Optional[bool] = None) -> None:
        self.id = id  # int
        self.history_deleted = history_deleted  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EncryptedChatDiscarded":
        
        flags = Int.read(b)
        
        history_deleted = True if flags & (1 << 0) else False
        id = Int.read(b)
        
        return EncryptedChatDiscarded(id=id, history_deleted=history_deleted)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.history_deleted else 0
        b.write(Int(flags))
        
        b.write(Int(self.id))
        
        return b.getvalue()
