from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class DismissSuggestion(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "suggestion"]

    ID = 0xf50dbaa1
    QUALNAME = "functions.help.DismissSuggestion"

    def __init__(self, *, peer: "raw.base.InputPeer", suggestion: str) -> None:
        self.peer = peer  # InputPeer
        self.suggestion = suggestion  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DismissSuggestion":
        # No flags
        
        peer = TLObject.read(b)
        
        suggestion = String.read(b)
        
        return DismissSuggestion(peer=peer, suggestion=suggestion)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(String(self.suggestion))
        
        return b.getvalue()
