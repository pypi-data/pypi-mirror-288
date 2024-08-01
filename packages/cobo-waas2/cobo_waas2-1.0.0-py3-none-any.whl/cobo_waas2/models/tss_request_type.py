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


class TSSRequestType(str, Enum):
    """
    The TSS request type. Possible values include: - `KeyGen`: This is a key generation request to create a [root extended public key](https://manuals.cobo.com/en/portal/mpc-wallets/ocw/tss-node-deployment#tss-node-on-cobo-portal-and-mpc-root-extended-public-key) and key shares for your [Main Group](https://manuals.cobo.com/en/portal/mpc-wallets/ocw/create-key-share-groups) after you've created the Main Group with [Create key share holder group](/v2/api-references/wallets--mpc-wallets/create-key-share-holder-group). You only need to do this once per [organization](https://manuals.cobo.com/en/portal/organization/introduction).  - `KeyGenFromKeyGroup`: This is a request to use the [Main Group](https://manuals.cobo.com/en/portal/mpc-wallets/ocw/create-key-share-groups) to create key shares for your [Signing Group](https://manuals.cobo.com/en/portal/mpc-wallets/ocw/create-key-share-groups) or [Recovery Group](https://manuals.cobo.com/en/portal/mpc-wallets/ocw/create-key-share-groups) after you've created these key share holder groups with [Create key share holder group](/v2/api-references/wallets--mpc-wallets/create-key-share-holder-group).  - `Recovery`: This is a request to create key shares using the [Recovery Group](https://manuals.cobo.com/en/portal/mpc-wallets/ocw/create-key-share-groups) for a key share holder in the [Main Group](https://manuals.cobo.com/en/portal/mpc-wallets/ocw/create-key-share-groups) if their key share has been lost (e.g. by losing their phone). 
    """

    """
    allowed enum values
    """
    KEYGEN = 'KeyGen'
    KEYGENFROMKEYGROUP = 'KeyGenFromKeyGroup'
    RECOVERY = 'Recovery'

    UNKNOWN = None

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of TSSRequestType from a JSON string"""
        return cls(json.loads(json_str))

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


