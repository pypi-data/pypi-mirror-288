from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetStarsTransactionsByID(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "id"]

    ID = 0x27842d2e
    QUALNAME = "functions.payments.GetStarsTransactionsByID"

    def __init__(self, *, peer: "raw.base.InputPeer", id: List["raw.base.InputStarsTransaction"]) -> None:
        self.peer = peer  # InputPeer
        self.id = id  # Vector<InputStarsTransaction>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetStarsTransactionsByID":
        # No flags
        
        peer = TLObject.read(b)
        
        id = TLObject.read(b)
        
        return GetStarsTransactionsByID(peer=peer, id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Vector(self.id))
        
        return b.getvalue()
