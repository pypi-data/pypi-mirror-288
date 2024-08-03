from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class InstallWallPaper(TLObject):  # type: ignore
    __slots__: List[str] = ["wallpaper", "settings"]

    ID = 0xfeed5769
    QUALNAME = "functions.account.InstallWallPaper"

    def __init__(self, *, wallpaper: "raw.base.InputWallPaper", settings: "raw.base.WallPaperSettings") -> None:
        self.wallpaper = wallpaper  # InputWallPaper
        self.settings = settings  # WallPaperSettings

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InstallWallPaper":
        # No flags
        
        wallpaper = TLObject.read(b)
        
        settings = TLObject.read(b)
        
        return InstallWallPaper(wallpaper=wallpaper, settings=settings)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.wallpaper.write())
        
        b.write(self.settings.write())
        
        return b.getvalue()
