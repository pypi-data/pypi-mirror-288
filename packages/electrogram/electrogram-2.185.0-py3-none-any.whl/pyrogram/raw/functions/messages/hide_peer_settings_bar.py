from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class HidePeerSettingsBar(TLObject):  # type: ignore
    __slots__: List[str] = ["peer"]

    ID = 0x4facb138
    QUALNAME = "functions.messages.HidePeerSettingsBar"

    def __init__(self, *, peer: "raw.base.InputPeer") -> None:
        self.peer = peer  # InputPeer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "HidePeerSettingsBar":
        # No flags
        
        peer = TLObject.read(b)
        
        return HidePeerSettingsBar(peer=peer)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        return b.getvalue()
