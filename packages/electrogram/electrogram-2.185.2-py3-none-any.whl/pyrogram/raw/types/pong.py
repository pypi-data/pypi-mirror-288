from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class Pong(TLObject):  # type: ignore
    __slots__: List[str] = ["msg_id", "ping_id"]

    ID = 0x347773c5
    QUALNAME = "types.Pong"

    def __init__(self, *, msg_id: int, ping_id: int) -> None:
        self.msg_id = msg_id  # long
        self.ping_id = ping_id  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Pong":
        # No flags
        
        msg_id = Long.read(b)
        
        ping_id = Long.read(b)
        
        return Pong(msg_id=msg_id, ping_id=ping_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.msg_id))
        
        b.write(Long(self.ping_id))
        
        return b.getvalue()
