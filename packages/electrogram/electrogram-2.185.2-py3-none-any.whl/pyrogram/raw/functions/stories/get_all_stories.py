from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetAllStories(TLObject):  # type: ignore
    __slots__: List[str] = ["next", "hidden", "state"]

    ID = 0xeeb0d625
    QUALNAME = "functions.stories.GetAllStories"

    def __init__(self, *, next: Optional[bool] = None, hidden: Optional[bool] = None, state: Optional[str] = None) -> None:
        self.next = next  # flags.1?true
        self.hidden = hidden  # flags.2?true
        self.state = state  # flags.0?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetAllStories":
        
        flags = Int.read(b)
        
        next = True if flags & (1 << 1) else False
        hidden = True if flags & (1 << 2) else False
        state = String.read(b) if flags & (1 << 0) else None
        return GetAllStories(next=next, hidden=hidden, state=state)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.next else 0
        flags |= (1 << 2) if self.hidden else 0
        flags |= (1 << 0) if self.state is not None else 0
        b.write(Int(flags))
        
        if self.state is not None:
            b.write(String(self.state))
        
        return b.getvalue()
