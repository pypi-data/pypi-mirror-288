from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetBotCallbackAnswer(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "msg_id", "game", "data", "password"]

    ID = 0x9342ca07
    QUALNAME = "functions.messages.GetBotCallbackAnswer"

    def __init__(self, *, peer: "raw.base.InputPeer", msg_id: int, game: Optional[bool] = None, data: Optional[bytes] = None, password: "raw.base.InputCheckPasswordSRP" = None) -> None:
        self.peer = peer  # InputPeer
        self.msg_id = msg_id  # int
        self.game = game  # flags.1?true
        self.data = data  # flags.0?bytes
        self.password = password  # flags.2?InputCheckPasswordSRP

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetBotCallbackAnswer":
        
        flags = Int.read(b)
        
        game = True if flags & (1 << 1) else False
        peer = TLObject.read(b)
        
        msg_id = Int.read(b)
        
        data = Bytes.read(b) if flags & (1 << 0) else None
        password = TLObject.read(b) if flags & (1 << 2) else None
        
        return GetBotCallbackAnswer(peer=peer, msg_id=msg_id, game=game, data=data, password=password)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.game else 0
        flags |= (1 << 0) if self.data is not None else 0
        flags |= (1 << 2) if self.password is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(Int(self.msg_id))
        
        if self.data is not None:
            b.write(Bytes(self.data))
        
        if self.password is not None:
            b.write(self.password.write())
        
        return b.getvalue()
