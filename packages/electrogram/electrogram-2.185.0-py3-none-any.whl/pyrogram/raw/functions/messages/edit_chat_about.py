from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class EditChatAbout(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "about"]

    ID = 0xdef60797
    QUALNAME = "functions.messages.EditChatAbout"

    def __init__(self, *, peer: "raw.base.InputPeer", about: str) -> None:
        self.peer = peer  # InputPeer
        self.about = about  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EditChatAbout":
        # No flags
        
        peer = TLObject.read(b)
        
        about = String.read(b)
        
        return EditChatAbout(peer=peer, about=about)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(String(self.about))
        
        return b.getvalue()
