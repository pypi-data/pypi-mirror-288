from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class LeaveChatlist(TLObject):  # type: ignore
    __slots__: List[str] = ["chatlist", "peers"]

    ID = 0x74fae13a
    QUALNAME = "functions.chatlists.LeaveChatlist"

    def __init__(self, *, chatlist: "raw.base.InputChatlist", peers: List["raw.base.InputPeer"]) -> None:
        self.chatlist = chatlist  # InputChatlist
        self.peers = peers  # Vector<InputPeer>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "LeaveChatlist":
        # No flags
        
        chatlist = TLObject.read(b)
        
        peers = TLObject.read(b)
        
        return LeaveChatlist(chatlist=chatlist, peers=peers)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.chatlist.write())
        
        b.write(Vector(self.peers))
        
        return b.getvalue()
