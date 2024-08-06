import datetime
from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="OnlineUserModModel")


@_attrs_define
class OnlineUserModModel:
    """
    Attributes:
        username (Union[None, Unset, str]):
        user_id (Union[None, Unset, str]):
        updated_on (Union[Unset, datetime.datetime]):
    """

    username: Union[None, Unset, str] = UNSET
    user_id: Union[None, Unset, str] = UNSET
    updated_on: Union[Unset, datetime.datetime] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        username: Union[None, Unset, str]
        if isinstance(self.username, Unset):
            username = UNSET
        else:
            username = self.username

        user_id: Union[None, Unset, str]
        if isinstance(self.user_id, Unset):
            user_id = UNSET
        else:
            user_id = self.user_id

        updated_on: Union[Unset, str] = UNSET
        if not isinstance(self.updated_on, Unset):
            updated_on = self.updated_on.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if username is not UNSET:
            field_dict["username"] = username
        if user_id is not UNSET:
            field_dict["userId"] = user_id
        if updated_on is not UNSET:
            field_dict["updatedOn"] = updated_on

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_username(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        username = _parse_username(d.pop("username", UNSET))

        def _parse_user_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_id = _parse_user_id(d.pop("userId", UNSET))

        _updated_on = d.pop("updatedOn", UNSET)
        updated_on: Union[Unset, datetime.datetime]
        if isinstance(_updated_on, Unset):
            updated_on = UNSET
        else:
            updated_on = isoparse(_updated_on)

        online_user_mod_model = cls(
            username=username,
            user_id=user_id,
            updated_on=updated_on,
        )

        return online_user_mod_model
