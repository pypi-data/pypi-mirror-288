# coding: utf-8

"""
    Cobo Wallet as a Service 2.0

    The version of the OpenAPI document: 1.0.0
    Contact: support@cobo.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from cobo_waas2.models.wallet_type import WalletType
from typing import Optional, Set
from typing_extensions import Self


class UpdateExchangeWalletParams(BaseModel):
    """
    The information of Exchange Wallets.
    """  # noqa: E501
    wallet_type: WalletType
    name: Optional[StrictStr] = Field(default=None, description="The wallet name.")
    apikey: Optional[StrictStr] = Field(default=None, description="The API key of your exchange account. This property is required when updating the information of an Exchange Wallet.")
    secret: Optional[StrictStr] = Field(default=None, description="The API secret of your exchange account. This property is required when updating the information of an Exchange Wallet.")
    passphrase: Optional[StrictStr] = Field(default=None, description="The passphrase of your exchange account.")
    memo: Optional[StrictStr] = Field(default=None, description="The memo you use when applying for the API key of your exchange account.")
    account_identify: Optional[StrictStr] = Field(default=None, description="The identifier of your exchange account. - For Binance, this is email address of your exchange account. - For OKX, this is the user name of your exchange account. ")
    ga_code: Optional[StrictStr] = Field(default=None, description="The GA code for the exchange.")
    main_wallet_id: Optional[StrictStr] = Field(default=None, description="The ID of the Exchange Wallet (Main Account).")
    __properties: ClassVar[List[str]] = ["wallet_type", "name", "apikey", "secret", "passphrase", "memo", "account_identify", "ga_code", "main_wallet_id"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of UpdateExchangeWalletParams from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UpdateExchangeWalletParams from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "wallet_type": obj.get("wallet_type"),
            "name": obj.get("name"),
            "apikey": obj.get("apikey"),
            "secret": obj.get("secret"),
            "passphrase": obj.get("passphrase"),
            "memo": obj.get("memo"),
            "account_identify": obj.get("account_identify"),
            "ga_code": obj.get("ga_code"),
            "main_wallet_id": obj.get("main_wallet_id")
        })
        return _obj


