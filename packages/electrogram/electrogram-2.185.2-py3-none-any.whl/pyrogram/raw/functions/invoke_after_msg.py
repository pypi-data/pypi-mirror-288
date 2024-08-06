from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class InvokeAfterMsg(TLObject):  # type: ignore
    __slots__: List[str] = ["msg_id", "query"]

    ID = 0xcb9f372d
    QUALNAME = "functions.InvokeAfterMsg"

    def __init__(self, *, msg_id: int, query: TLObject) -> None:
        self.msg_id = msg_id  # long
        self.query = query  # !X

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InvokeAfterMsg":
        # No flags
        
        msg_id = Long.read(b)
        
        query = TLObject.read(b)
        
        return InvokeAfterMsg(msg_id=msg_id, query=query)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.msg_id))
        
        b.write(self.query.write())
        
        return b.getvalue()
