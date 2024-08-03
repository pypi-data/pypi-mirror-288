from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetUserBoosts(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "user_id"]

    ID = 0x39854d1f
    QUALNAME = "functions.premium.GetUserBoosts"

    def __init__(self, *, peer: "raw.base.InputPeer", user_id: "raw.base.InputUser") -> None:
        self.peer = peer  # InputPeer
        self.user_id = user_id  # InputUser

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetUserBoosts":
        # No flags
        
        peer = TLObject.read(b)
        
        user_id = TLObject.read(b)
        
        return GetUserBoosts(peer=peer, user_id=user_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.user_id.write())
        
        return b.getvalue()
