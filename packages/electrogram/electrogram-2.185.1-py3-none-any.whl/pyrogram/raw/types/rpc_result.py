from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class RpcResult(TLObject):  # type: ignore
    __slots__: List[str] = ["req_msg_id", "result"]

    ID = 0xf35c6d01
    QUALNAME = "types.RpcResult"

    def __init__(self, *, req_msg_id: int, result: TLObject) -> None:
        self.req_msg_id = req_msg_id  # long
        self.result = result  # Object

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "RpcResult":
        # No flags
        
        req_msg_id = Long.read(b)
        
        result = TLObject.read(b)
        
        return RpcResult(req_msg_id=req_msg_id, result=result)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.req_msg_id))
        
        b.write(self.result.write())
        
        return b.getvalue()
