# coding: utf-8

"""
    Cobo Wallet as a Service 2.0

    The version of the OpenAPI document: 1.0.0
    Contact: support@cobo.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class MPCVaultType(str, Enum):
    """
    The vault type. Possible values include: - `Org-Controlled`: This vault is a collection of [Organization-Controlled Wallets](https://manuals.cobo.com/en/portal/mpc-wallets/introduction#organization-controlled-wallets).  - `User-Controlled`: This vault is a collection of [User-Controlled Wallets](https://manuals.cobo.com/en/portal/mpc-wallets/introduction#user-controlled-wallets). 
    """

    """
    allowed enum values
    """
    ORG_MINUS_CONTROLLED = 'Org-Controlled'
    USER_MINUS_CONTROLLED = 'User-Controlled'

    UNKNOWN = None

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of MPCVaultType from a JSON string"""
        return cls(json.loads(json_str))

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


