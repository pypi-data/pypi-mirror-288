from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class UpdatePeerLocated(TLObject):  # type: ignore
    __slots__: List[str] = ["peers"]

    ID = 0xb4afcfb0
    QUALNAME = "types.UpdatePeerLocated"

    def __init__(self, *, peers: List["raw.base.PeerLocated"]) -> None:
        self.peers = peers  # Vector<PeerLocated>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdatePeerLocated":
        # No flags
        
        peers = TLObject.read(b)
        
        return UpdatePeerLocated(peers=peers)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.peers))
        
        return b.getvalue()
