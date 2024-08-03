from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class PQInnerDataTemp(TLObject):  # type: ignore
    __slots__: List[str] = ["pq", "p", "q", "nonce", "server_nonce", "new_nonce", "expires_in"]

    ID = 0x3c6a84d4
    QUALNAME = "types.PQInnerDataTemp"

    def __init__(self, *, pq: bytes, p: bytes, q: bytes, nonce: int, server_nonce: int, new_nonce: int, expires_in: int) -> None:
        self.pq = pq  # bytes
        self.p = p  # bytes
        self.q = q  # bytes
        self.nonce = nonce  # int128
        self.server_nonce = server_nonce  # int128
        self.new_nonce = new_nonce  # int256
        self.expires_in = expires_in  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PQInnerDataTemp":
        # No flags
        
        pq = Bytes.read(b)
        
        p = Bytes.read(b)
        
        q = Bytes.read(b)
        
        nonce = Int128.read(b)
        
        server_nonce = Int128.read(b)
        
        new_nonce = Int256.read(b)
        
        expires_in = Int.read(b)
        
        return PQInnerDataTemp(pq=pq, p=p, q=q, nonce=nonce, server_nonce=server_nonce, new_nonce=new_nonce, expires_in=expires_in)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.pq))
        
        b.write(Bytes(self.p))
        
        b.write(Bytes(self.q))
        
        b.write(Int128(self.nonce))
        
        b.write(Int128(self.server_nonce))
        
        b.write(Int256(self.new_nonce))
        
        b.write(Int(self.expires_in))
        
        return b.getvalue()
