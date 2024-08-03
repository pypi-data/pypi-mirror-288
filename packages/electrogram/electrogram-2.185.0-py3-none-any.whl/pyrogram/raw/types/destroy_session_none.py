from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class DestroySessionNone(TLObject):  # type: ignore
    __slots__: List[str] = ["session_id"]

    ID = 0x62d350c9
    QUALNAME = "types.DestroySessionNone"

    def __init__(self, *, session_id: int) -> None:
        self.session_id = session_id  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DestroySessionNone":
        # No flags
        
        session_id = Long.read(b)
        
        return DestroySessionNone(session_id=session_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.session_id))
        
        return b.getvalue()
