from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ChatlistInvite(TLObject):  # type: ignore
    __slots__: List[str] = ["title", "peers", "chats", "users", "emoticon"]

    ID = 0x1dcd839d
    QUALNAME = "types.chatlists.ChatlistInvite"

    def __init__(self, *, title: str, peers: List["raw.base.Peer"], chats: List["raw.base.Chat"], users: List["raw.base.User"], emoticon: Optional[str] = None) -> None:
        self.title = title  # string
        self.peers = peers  # Vector<Peer>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.emoticon = emoticon  # flags.0?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChatlistInvite":
        
        flags = Int.read(b)
        
        title = String.read(b)
        
        emoticon = String.read(b) if flags & (1 << 0) else None
        peers = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return ChatlistInvite(title=title, peers=peers, chats=chats, users=users, emoticon=emoticon)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.emoticon is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.title))
        
        if self.emoticon is not None:
            b.write(String(self.emoticon))
        
        b.write(Vector(self.peers))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
