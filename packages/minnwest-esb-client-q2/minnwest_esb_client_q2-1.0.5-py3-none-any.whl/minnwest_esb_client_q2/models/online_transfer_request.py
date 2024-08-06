from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.transfer_frequency import TransferFrequency
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.online_user_mod_model import OnlineUserModModel


T = TypeVar("T", bound="OnlineTransferRequest")


@_attrs_define
class OnlineTransferRequest:
    """
    Attributes:
        user (Union[Unset, OnlineUserModModel]):
        from_account_number (Union[None, Unset, str]):
        to_account_number (Union[None, Unset, str]):
        portfolio_name_line (Union[None, Unset, str]):
        amount (Union[Unset, float]):
        frequency (Union[Unset, TransferFrequency]):
        memo (Union[None, Unset, str]):
    """

    user: Union[Unset, "OnlineUserModModel"] = UNSET
    from_account_number: Union[None, Unset, str] = UNSET
    to_account_number: Union[None, Unset, str] = UNSET
    portfolio_name_line: Union[None, Unset, str] = UNSET
    amount: Union[Unset, float] = UNSET
    frequency: Union[Unset, TransferFrequency] = UNSET
    memo: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        from_account_number: Union[None, Unset, str]
        if isinstance(self.from_account_number, Unset):
            from_account_number = UNSET
        else:
            from_account_number = self.from_account_number

        to_account_number: Union[None, Unset, str]
        if isinstance(self.to_account_number, Unset):
            to_account_number = UNSET
        else:
            to_account_number = self.to_account_number

        portfolio_name_line: Union[None, Unset, str]
        if isinstance(self.portfolio_name_line, Unset):
            portfolio_name_line = UNSET
        else:
            portfolio_name_line = self.portfolio_name_line

        amount = self.amount

        frequency: Union[Unset, str] = UNSET
        if not isinstance(self.frequency, Unset):
            frequency = self.frequency.value

        memo: Union[None, Unset, str]
        if isinstance(self.memo, Unset):
            memo = UNSET
        else:
            memo = self.memo

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if user is not UNSET:
            field_dict["user"] = user
        if from_account_number is not UNSET:
            field_dict["fromAccountNumber"] = from_account_number
        if to_account_number is not UNSET:
            field_dict["toAccountNumber"] = to_account_number
        if portfolio_name_line is not UNSET:
            field_dict["portfolioNameLine"] = portfolio_name_line
        if amount is not UNSET:
            field_dict["amount"] = amount
        if frequency is not UNSET:
            field_dict["frequency"] = frequency
        if memo is not UNSET:
            field_dict["memo"] = memo

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.online_user_mod_model import OnlineUserModModel

        d = src_dict.copy()
        _user = d.pop("user", UNSET)
        user: Union[Unset, OnlineUserModModel]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = OnlineUserModModel.from_dict(_user)

        def _parse_from_account_number(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        from_account_number = _parse_from_account_number(d.pop("fromAccountNumber", UNSET))

        def _parse_to_account_number(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        to_account_number = _parse_to_account_number(d.pop("toAccountNumber", UNSET))

        def _parse_portfolio_name_line(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        portfolio_name_line = _parse_portfolio_name_line(d.pop("portfolioNameLine", UNSET))

        amount = d.pop("amount", UNSET)

        _frequency = d.pop("frequency", UNSET)
        frequency: Union[Unset, TransferFrequency]
        if isinstance(_frequency, Unset):
            frequency = UNSET
        else:
            frequency = TransferFrequency(_frequency)

        def _parse_memo(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        memo = _parse_memo(d.pop("memo", UNSET))

        online_transfer_request = cls(
            user=user,
            from_account_number=from_account_number,
            to_account_number=to_account_number,
            portfolio_name_line=portfolio_name_line,
            amount=amount,
            frequency=frequency,
            memo=memo,
        )

        return online_transfer_request
