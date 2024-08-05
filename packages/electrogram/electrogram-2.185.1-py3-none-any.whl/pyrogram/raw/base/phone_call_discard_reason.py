from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PhoneCallDiscardReason = Union["raw.types.PhoneCallDiscardReasonBusy", "raw.types.PhoneCallDiscardReasonDisconnect", "raw.types.PhoneCallDiscardReasonHangup", "raw.types.PhoneCallDiscardReasonMissed"]


# noinspection PyRedeclaration
class PhoneCallDiscardReason:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PhoneCallDiscardReason"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
