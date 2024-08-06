from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SetChatAvailableReactions(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "available_reactions", "reactions_limit"]

    ID = 0x5a150bd4
    QUALNAME = "functions.messages.SetChatAvailableReactions"

    def __init__(self, *, peer: "raw.base.InputPeer", available_reactions: "raw.base.ChatReactions", reactions_limit: Optional[int] = None) -> None:
        self.peer = peer  # InputPeer
        self.available_reactions = available_reactions  # ChatReactions
        self.reactions_limit = reactions_limit  # flags.0?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SetChatAvailableReactions":
        
        flags = Int.read(b)
        
        peer = TLObject.read(b)
        
        available_reactions = TLObject.read(b)
        
        reactions_limit = Int.read(b) if flags & (1 << 0) else None
        return SetChatAvailableReactions(peer=peer, available_reactions=available_reactions, reactions_limit=reactions_limit)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.reactions_limit is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(self.available_reactions.write())
        
        if self.reactions_limit is not None:
            b.write(Int(self.reactions_limit))
        
        return b.getvalue()
