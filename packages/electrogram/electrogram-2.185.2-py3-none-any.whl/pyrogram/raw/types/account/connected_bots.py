from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ConnectedBots(TLObject):  # type: ignore
    __slots__: List[str] = ["connected_bots", "users"]

    ID = 0x17d7f87b
    QUALNAME = "types.account.ConnectedBots"

    def __init__(self, *, connected_bots: List["raw.base.ConnectedBot"], users: List["raw.base.User"]) -> None:
        self.connected_bots = connected_bots  # Vector<ConnectedBot>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ConnectedBots":
        # No flags
        
        connected_bots = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return ConnectedBots(connected_bots=connected_bots, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.connected_bots))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
