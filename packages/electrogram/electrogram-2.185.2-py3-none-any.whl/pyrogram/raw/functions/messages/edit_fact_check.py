from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class EditFactCheck(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "msg_id", "text"]

    ID = 0x589ee75
    QUALNAME = "functions.messages.EditFactCheck"

    def __init__(self, *, peer: "raw.base.InputPeer", msg_id: int, text: "raw.base.TextWithEntities") -> None:
        self.peer = peer  # InputPeer
        self.msg_id = msg_id  # int
        self.text = text  # TextWithEntities

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EditFactCheck":
        # No flags
        
        peer = TLObject.read(b)
        
        msg_id = Int.read(b)
        
        text = TLObject.read(b)
        
        return EditFactCheck(peer=peer, msg_id=msg_id, text=text)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.msg_id))
        
        b.write(self.text.write())
        
        return b.getvalue()
