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
import pprint
from pydantic import BaseModel, ConfigDict, Field, StrictStr, ValidationError, field_validator
from typing import Any, List, Optional
from cobo_waas2.models.transaction_request_evm_eip1559_fee import TransactionRequestEvmEip1559Fee
from cobo_waas2.models.transaction_request_evm_legacy_fee import TransactionRequestEvmLegacyFee
from cobo_waas2.models.transaction_request_fixed_fee import TransactionRequestFixedFee
from cobo_waas2.models.transaction_request_utxo_fee import TransactionRequestUtxoFee
from pydantic import StrictStr, Field
from typing import Union, List, Set, Optional, Dict
from typing_extensions import Literal, Self

TRANSACTIONREQUESTFEE_ONE_OF_SCHEMAS = ["TransactionRequestEvmEip1559Fee", "TransactionRequestEvmLegacyFee", "TransactionRequestFixedFee", "TransactionRequestUtxoFee"]

class TransactionRequestFee(BaseModel):
    """
    TransactionRequestFee
    """
    # data type: TransactionRequestFixedFee
    oneof_schema_1_validator: Optional[TransactionRequestFixedFee] = None
    # data type: TransactionRequestEvmEip1559Fee
    oneof_schema_2_validator: Optional[TransactionRequestEvmEip1559Fee] = None
    # data type: TransactionRequestEvmLegacyFee
    oneof_schema_3_validator: Optional[TransactionRequestEvmLegacyFee] = None
    # data type: TransactionRequestUtxoFee
    oneof_schema_4_validator: Optional[TransactionRequestUtxoFee] = None
    actual_instance: Optional[Union[TransactionRequestEvmEip1559Fee, TransactionRequestEvmLegacyFee, TransactionRequestFixedFee, TransactionRequestUtxoFee]] = None
    one_of_schemas: Set[str] = { "TransactionRequestEvmEip1559Fee", "TransactionRequestEvmLegacyFee", "TransactionRequestFixedFee", "TransactionRequestUtxoFee" }

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )


    discriminator_value_class_map: Dict[str, str] = {
    }

    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator('actual_instance')
    def actual_instance_must_validate_oneof(cls, v):
        instance = TransactionRequestFee.model_construct()
        error_messages = []
        match = 0
        # validate data type: TransactionRequestFixedFee
        if not isinstance(v, TransactionRequestFixedFee):
            error_messages.append(f"Error! Input type `{type(v)}` is not `TransactionRequestFixedFee`")
        else:
            match += 1
        # validate data type: TransactionRequestEvmEip1559Fee
        if not isinstance(v, TransactionRequestEvmEip1559Fee):
            error_messages.append(f"Error! Input type `{type(v)}` is not `TransactionRequestEvmEip1559Fee`")
        else:
            match += 1
        # validate data type: TransactionRequestEvmLegacyFee
        if not isinstance(v, TransactionRequestEvmLegacyFee):
            error_messages.append(f"Error! Input type `{type(v)}` is not `TransactionRequestEvmLegacyFee`")
        else:
            match += 1
        # validate data type: TransactionRequestUtxoFee
        if not isinstance(v, TransactionRequestUtxoFee):
            error_messages.append(f"Error! Input type `{type(v)}` is not `TransactionRequestUtxoFee`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in TransactionRequestFee with oneOf schemas: TransactionRequestEvmEip1559Fee, TransactionRequestEvmLegacyFee, TransactionRequestFixedFee, TransactionRequestUtxoFee. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in TransactionRequestFee with oneOf schemas: TransactionRequestEvmEip1559Fee, TransactionRequestEvmLegacyFee, TransactionRequestFixedFee, TransactionRequestUtxoFee. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Union[str, Dict[str, Any]]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        match = 0

        # use oneOf discriminator to lookup the data type
        _data_type = json.loads(json_str).get("fee_type")
        if not _data_type:
            raise ValueError("Failed to lookup data type from the field `fee_type` in the input.")

        # check if data type is `TransactionRequestEvmEip1559Fee`
        if _data_type == "EVM_EIP_1559":
            instance.actual_instance = TransactionRequestEvmEip1559Fee.from_json(json_str)
            return instance

        # check if data type is `TransactionRequestEvmLegacyFee`
        if _data_type == "EVM_Legacy":
            instance.actual_instance = TransactionRequestEvmLegacyFee.from_json(json_str)
            return instance

        # check if data type is `TransactionRequestFixedFee`
        if _data_type == "Fixed":
            instance.actual_instance = TransactionRequestFixedFee.from_json(json_str)
            return instance

        # check if data type is `TransactionRequestUtxoFee`
        if _data_type == "UTXO":
            instance.actual_instance = TransactionRequestUtxoFee.from_json(json_str)
            return instance

        # check if data type is `TransactionRequestEvmEip1559Fee`
        if _data_type == "TransactionRequestEvmEip1559Fee":
            instance.actual_instance = TransactionRequestEvmEip1559Fee.from_json(json_str)
            return instance

        # check if data type is `TransactionRequestEvmLegacyFee`
        if _data_type == "TransactionRequestEvmLegacyFee":
            instance.actual_instance = TransactionRequestEvmLegacyFee.from_json(json_str)
            return instance

        # check if data type is `TransactionRequestFixedFee`
        if _data_type == "TransactionRequestFixedFee":
            instance.actual_instance = TransactionRequestFixedFee.from_json(json_str)
            return instance

        # check if data type is `TransactionRequestUtxoFee`
        if _data_type == "TransactionRequestUtxoFee":
            instance.actual_instance = TransactionRequestUtxoFee.from_json(json_str)
            return instance

        # deserialize data into TransactionRequestFixedFee
        try:
            instance.actual_instance = TransactionRequestFixedFee.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into TransactionRequestEvmEip1559Fee
        try:
            instance.actual_instance = TransactionRequestEvmEip1559Fee.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into TransactionRequestEvmLegacyFee
        try:
            instance.actual_instance = TransactionRequestEvmLegacyFee.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into TransactionRequestUtxoFee
        try:
            instance.actual_instance = TransactionRequestUtxoFee.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into TransactionRequestFee with oneOf schemas: TransactionRequestEvmEip1559Fee, TransactionRequestEvmLegacyFee, TransactionRequestFixedFee, TransactionRequestUtxoFee. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            return instance
            # raise ValueError("No match found when deserializing the JSON string into TransactionRequestFee with oneOf schemas: TransactionRequestEvmEip1559Fee, TransactionRequestEvmLegacyFee, TransactionRequestFixedFee, TransactionRequestUtxoFee. Details: " + ", ".join(error_messages))
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(self.actual_instance.to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(self) -> Optional[Union[Dict[str, Any], TransactionRequestEvmEip1559Fee, TransactionRequestEvmLegacyFee, TransactionRequestFixedFee, TransactionRequestUtxoFee]]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            # primitive type
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())


