from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SendScreenshotNotification(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "reply_to", "random_id"]

    ID = 0xa1405817
    QUALNAME = "functions.messages.SendScreenshotNotification"

    def __init__(self, *, peer: "raw.base.InputPeer", reply_to: "raw.base.InputReplyTo", random_id: int) -> None:
        self.peer = peer  # InputPeer
        self.reply_to = reply_to  # InputReplyTo
        self.random_id = random_id  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendScreenshotNotification":
        # No flags
        
        peer = TLObject.read(b)
        
        reply_to = TLObject.read(b)
        
        random_id = Long.read(b)
        
        return SendScreenshotNotification(peer=peer, reply_to=reply_to, random_id=random_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.reply_to.write())
        
        b.write(Long(self.random_id))
        
        return b.getvalue()
