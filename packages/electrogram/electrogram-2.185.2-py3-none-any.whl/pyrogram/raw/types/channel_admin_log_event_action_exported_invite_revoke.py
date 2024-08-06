from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ChannelAdminLogEventActionExportedInviteRevoke(TLObject):  # type: ignore
    __slots__: List[str] = ["invite"]

    ID = 0x410a134e
    QUALNAME = "types.ChannelAdminLogEventActionExportedInviteRevoke"

    def __init__(self, *, invite: "raw.base.ExportedChatInvite") -> None:
        self.invite = invite  # ExportedChatInvite

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelAdminLogEventActionExportedInviteRevoke":
        # No flags
        
        invite = TLObject.read(b)
        
        return ChannelAdminLogEventActionExportedInviteRevoke(invite=invite)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.invite.write())
        
        return b.getvalue()
