from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class DeleteQuickReplyMessages(TLObject):  # type: ignore
    __slots__: List[str] = ["shortcut_id", "id"]

    ID = 0xe105e910
    QUALNAME = "functions.messages.DeleteQuickReplyMessages"

    def __init__(self, *, shortcut_id: int, id: List[int]) -> None:
        self.shortcut_id = shortcut_id  # int
        self.id = id  # Vector<int>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DeleteQuickReplyMessages":
        # No flags
        
        shortcut_id = Int.read(b)
        
        id = TLObject.read(b, Int)
        
        return DeleteQuickReplyMessages(shortcut_id=shortcut_id, id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.shortcut_id))
        
        b.write(Vector(self.id, Int))
        
        return b.getvalue()
