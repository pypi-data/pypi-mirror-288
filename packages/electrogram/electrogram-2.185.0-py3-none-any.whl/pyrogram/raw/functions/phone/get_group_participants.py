from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetGroupParticipants(TLObject):  # type: ignore
    __slots__: List[str] = ["call", "ids", "sources", "offset", "limit"]

    ID = 0xc558d8ab
    QUALNAME = "functions.phone.GetGroupParticipants"

    def __init__(self, *, call: "raw.base.InputGroupCall", ids: List["raw.base.InputPeer"], sources: List[int], offset: str, limit: int) -> None:
        self.call = call  # InputGroupCall
        self.ids = ids  # Vector<InputPeer>
        self.sources = sources  # Vector<int>
        self.offset = offset  # string
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetGroupParticipants":
        # No flags
        
        call = TLObject.read(b)
        
        ids = TLObject.read(b)
        
        sources = TLObject.read(b, Int)
        
        offset = String.read(b)
        
        limit = Int.read(b)
        
        return GetGroupParticipants(call=call, ids=ids, sources=sources, offset=offset, limit=limit)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.call.write())
        
        b.write(Vector(self.ids))
        
        b.write(Vector(self.sources, Int))
        
        b.write(String(self.offset))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
