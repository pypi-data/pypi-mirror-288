from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SecureValueType = Union["raw.types.SecureValueTypeAddress", "raw.types.SecureValueTypeBankStatement", "raw.types.SecureValueTypeDriverLicense", "raw.types.SecureValueTypeEmail", "raw.types.SecureValueTypeIdentityCard", "raw.types.SecureValueTypeInternalPassport", "raw.types.SecureValueTypePassport", "raw.types.SecureValueTypePassportRegistration", "raw.types.SecureValueTypePersonalDetails", "raw.types.SecureValueTypePhone", "raw.types.SecureValueTypeRentalAgreement", "raw.types.SecureValueTypeTemporaryRegistration", "raw.types.SecureValueTypeUtilityBill"]


# noinspection PyRedeclaration
class SecureValueType:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SecureValueType"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
