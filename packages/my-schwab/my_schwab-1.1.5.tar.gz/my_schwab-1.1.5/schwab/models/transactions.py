# Standard library imports
from dataclasses import dataclass
from datetime import date, datetime, timedelta

# Relative imports
from .meta import Mapping
from ..utils import binary_search, dict_to_snake, parse_date
from ..enums import *

_FIELDS = {
    'account_number',
    'activity_id',
    'position_id',
    'order_id',
    'type',
    'net_amount',
    'time',
    'status',
    'sub_account',
    'trade_date',
    'symbol',
    'fee',
    'value',
    'quantity',
    'position_effect',
    'price'
}

@dataclass(slots=True, kw_only=True, repr=False)
class Transaction(Mapping):
    account_number: int
    _transfer_items: list[dict]
    activity_id: int = None
    position_id: int = None
    order_id: int = None
    type: str = None
    net_amount: float = None
    time: datetime
    status: str = None
    sub_account: str = None
    trade_date: datetime = None
    symbol: str = None
    fee: float = None
    value: float = None
    quantity: float = None
    position_effect: str = None
    price: float = None

    def __post_init__(self):
        self.account_number = int(self.account_number)
        self.symbol = self._transfer_items[-1]['instrument']['symbol']

        fee = 0
        for item in self._transfer_items[:-1]:
            fee += item['amount']
        self.fee = round(fee, 2)

        self.quantity = self._transfer_items[-1]['amount']
        self.value = abs(self._transfer_items[-1]['cost'])
        self.price = self._transfer_items[-1]['price']
        self.position_effect = self._transfer_items[-1]['position_effect']

    def __repr__(self):
        fields = sorted(self.__dataclass_fields__.keys())
        fields.remove('_transfer_items')

        values = [f"{name}={getattr(self, name)}" for name in fields]

        return f"Transaction({', '.join(values)})"

    def __eq__(self, other):
        if not isinstance(other, Transaction):
            return False
        return self.order_id == other.order_id


@dataclass(slots=True, repr=False)
class Transactions:
    _data: list[Transaction]

    @property
    def transactions(self):
        return self._data

    def __post_init__(self):
        self._data = sorted([self._build_transaction(transaction) for transaction in self._data], key=lambda x: x.trade_date)

    def __repr__(self):
        return f"<Transactions: {len(self._data)} transactions>"

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __contains__(self, value):
        if isinstance(value, Transaction):
            return value in self._data
        try:
            value = self._build_transaction(value)
        except TypeError:
            return False
        return value in self._data

    def __getitem__(self, value):
        if isinstance(value, (int, slice)):
            return self._data[value]
        elif isinstance(value, tuple):
            return self.filter(*value)

    def _build_transaction(cls, transaction) -> Transaction:
        if isinstance(transaction, Transaction):
            return transaction
        values = dict_to_snake(transaction)
        values['_transfer_items'] = values.pop('transfer_items')
        return Transaction(**values)

    def today(self) -> "Transactions":
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return self.filter_by_date(today)

    def date(self, value) -> "Transactions":
        date = parse_date(value)
        return self.filter_by_date(date)

    def filter(self, by, value) -> "Transactions":
        if by not in _FIELDS:
            raise ValueError(f"'{by}' is not a valid field. Valid fields are: {_FIELDS}")

        if by == 'trade_date':
            return self.filter_by_date(value)

        elif by == 'symbol':
            return self.filter_by_symbol(value)

        elif by == 'order_id':
            return self.filter_by_order(value)

        else:
            return Transactions([transaction for transaction in self._data if getattr(transaction, by) == value])

    def filter_date(self, from_date=None, to_date=None) -> "Transactions":
        return self.filter_by_date(from_date, to_date)

    def filter_by_date(self, from_date=None, to_date=None) -> "Transactions":
        attr = 'trade_date'

        if (from_date := parse_date(from_date)) is None:
            from_date = parse_date(
                (datetime.now() - timedelta(days=365)).isoformat()
            )

        if (to_date := parse_date(to_date)) is None:
            to_date = from_date + timedelta(days=1)

        left_index = binary_search(self._data, from_date, attr, 'left')
        right_index = binary_search(self._data, to_date, attr, 'right')
        return Transactions(self._data[left_index:right_index])

    def filter_by_symbol(self, symbol) -> "Transactions":
        symbol = symbol.upper()
        return Transactions([transaction for transaction in self._data if transaction.symbol == symbol])

    def filter_by_order(self, order_ids) -> "Transactions":
        if isinstance(order_ids, (int, str)):
            order_ids = {int(order_ids)}
        return Transactions([transaction for transaction in self._data if transaction.order_id in order_ids])
