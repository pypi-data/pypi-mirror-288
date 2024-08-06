from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class DeleteExportedChatInvite(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "link"]

    ID = 0xd464a42b
    QUALNAME = "functions.messages.DeleteExportedChatInvite"

    def __init__(self, *, peer: "raw.base.InputPeer", link: str) -> None:
        self.peer = peer  # InputPeer
        self.link = link  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DeleteExportedChatInvite":
        # No flags
        
        peer = TLObject.read(b)
        
        link = String.read(b)
        
        return DeleteExportedChatInvite(peer=peer, link=link)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(String(self.link))
        
        return b.getvalue()
