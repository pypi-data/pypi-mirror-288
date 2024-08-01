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
from cobo_waas2.models.activity_type import ActivityType
from cobo_waas2.models.transaction_request_fee import TransactionRequestFee
from typing import Optional, Set
from typing_extensions import Self


class EstimateWithdrawFee(BaseModel):
    """
    EstimateWithdrawFee
    """  # noqa: E501
    activity_type: ActivityType
    staking_id: StrictStr = Field(description="The id of the related staking.")
    amount: Optional[StrictStr] = Field(default=None, description="The amount to stake")
    address: Optional[StrictStr] = Field(default=None, description="The withdraw to address.")
    fee: TransactionRequestFee
    __properties: ClassVar[List[str]] = ["activity_type", "staking_id", "amount", "address", "fee"]

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
        """Create an instance of EstimateWithdrawFee from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of fee
        if self.fee:
            _dict['fee'] = self.fee.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of EstimateWithdrawFee from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "activity_type": obj.get("activity_type"),
            "staking_id": obj.get("staking_id"),
            "amount": obj.get("amount"),
            "address": obj.get("address"),
            "fee": TransactionRequestFee.from_dict(obj["fee"]) if obj.get("fee") is not None else None
        })
        return _obj


