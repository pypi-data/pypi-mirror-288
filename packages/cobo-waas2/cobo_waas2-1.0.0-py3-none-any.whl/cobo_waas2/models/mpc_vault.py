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

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from cobo_waas2.models.mpc_vault_type import MPCVaultType
from cobo_waas2.models.root_pubkey import RootPubkey
from typing import Optional, Set
from typing_extensions import Self


class MPCVault(BaseModel):
    """
    The data for vault information.
    """  # noqa: E501
    vault_id: Optional[StrictStr] = Field(default=None, description="The vault ID.")
    project_id: Optional[StrictStr] = Field(default=None, description="The project ID.")
    name: Optional[StrictStr] = Field(default=None, description="The vault name.")
    type: Optional[MPCVaultType] = None
    root_pubkeys: Optional[List[RootPubkey]] = None
    create_timestamp: Optional[StrictInt] = Field(default=None, description="The vault's creation time in Unix timestamp format, measured in milliseconds.")
    __properties: ClassVar[List[str]] = ["vault_id", "project_id", "name", "type", "root_pubkeys", "create_timestamp"]

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
        """Create an instance of MPCVault from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in root_pubkeys (list)
        _items = []
        if self.root_pubkeys:
            for _item in self.root_pubkeys:
                if _item:
                    _items.append(_item.to_dict())
            _dict['root_pubkeys'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of MPCVault from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "vault_id": obj.get("vault_id"),
            "project_id": obj.get("project_id"),
            "name": obj.get("name"),
            "type": obj.get("type"),
            "root_pubkeys": [RootPubkey.from_dict(_item) for _item in obj["root_pubkeys"]] if obj.get("root_pubkeys") is not None else None,
            "create_timestamp": obj.get("create_timestamp")
        })
        return _obj


