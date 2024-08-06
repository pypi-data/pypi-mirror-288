from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Dict,
    Optional,
    TextIO,
    Tuple,
    Type,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import (
    UNSET,
    Unset,
)

T = TypeVar("T", bound="DatabaseSettings")


@_attrs_define
class DatabaseSettings:
    """ 
        Attributes:
            offload_enabled (bool):
     """

    offload_enabled: bool


    def to_dict(self) -> Dict[str, Any]:
        offload_enabled = self.offload_enabled


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "offloadEnabled": offload_enabled,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        offload_enabled = d.pop("offloadEnabled")

        database_settings = cls(
            offload_enabled=offload_enabled,
        )

        return database_settings

