from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class MsgsStateInfo(TLObject):  # type: ignore
    __slots__: List[str] = ["req_msg_id", "info"]

    ID = 0x04deb57d
    QUALNAME = "types.MsgsStateInfo"

    def __init__(self, *, req_msg_id: int, info: str) -> None:
        self.req_msg_id = req_msg_id  # long
        self.info = info  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MsgsStateInfo":
        # No flags
        
        req_msg_id = Long.read(b)
        
        info = String.read(b)
        
        return MsgsStateInfo(req_msg_id=req_msg_id, info=info)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.req_msg_id))
        
        b.write(String(self.info))
        
        return b.getvalue()
