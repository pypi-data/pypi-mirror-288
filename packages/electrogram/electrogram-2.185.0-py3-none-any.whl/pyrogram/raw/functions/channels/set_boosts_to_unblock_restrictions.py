from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SetBoostsToUnblockRestrictions(TLObject):  # type: ignore
    __slots__: List[str] = ["channel", "boosts"]

    ID = 0xad399cee
    QUALNAME = "functions.channels.SetBoostsToUnblockRestrictions"

    def __init__(self, *, channel: "raw.base.InputChannel", boosts: int) -> None:
        self.channel = channel  # InputChannel
        self.boosts = boosts  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SetBoostsToUnblockRestrictions":
        # No flags
        
        channel = TLObject.read(b)
        
        boosts = Int.read(b)
        
        return SetBoostsToUnblockRestrictions(channel=channel, boosts=boosts)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(Int(self.boosts))
        
        return b.getvalue()
