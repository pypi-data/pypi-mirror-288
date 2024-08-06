from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputStorePaymentPurpose = Union["raw.types.InputStorePaymentGiftPremium", "raw.types.InputStorePaymentPremiumGiftCode", "raw.types.InputStorePaymentPremiumGiveaway", "raw.types.InputStorePaymentPremiumSubscription", "raw.types.InputStorePaymentStarsGift", "raw.types.InputStorePaymentStarsTopup"]


# noinspection PyRedeclaration
class InputStorePaymentPurpose:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputStorePaymentPurpose"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
