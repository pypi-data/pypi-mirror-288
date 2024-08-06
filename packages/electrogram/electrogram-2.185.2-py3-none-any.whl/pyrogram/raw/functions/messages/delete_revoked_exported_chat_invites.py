from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class DeleteRevokedExportedChatInvites(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "admin_id"]

    ID = 0x56987bd5
    QUALNAME = "functions.messages.DeleteRevokedExportedChatInvites"

    def __init__(self, *, peer: "raw.base.InputPeer", admin_id: "raw.base.InputUser") -> None:
        self.peer = peer  # InputPeer
        self.admin_id = admin_id  # InputUser

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DeleteRevokedExportedChatInvites":
        # No flags
        
        peer = TLObject.read(b)
        
        admin_id = TLObject.read(b)
        
        return DeleteRevokedExportedChatInvites(peer=peer, admin_id=admin_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.admin_id.write())
        
        return b.getvalue()
