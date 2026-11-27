from dataclasses import dataclass, field 
from datetime import datetime 
from itertools import count

_next_id = count # gives each order a unique id

@dataclass
class Order:
    side: str # 'buy' or 'sell'
    price: int
    quantity: int
    id: int = field(default_factory=lambda: next(_next_id))
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        # ensures we're not dealing with bad values
        if self.side not in ("buy", "sell"):
            raise ValueError(f"side must be 'buy' or 'sell', got {self.side!r}")
        if self.price <= 0 or self.quantity <= 0:
            raise ValueError("prince and quantity must be positive")
        

@dataclass(frozen=True) # this should never change since a trade is a record of something that happened
class Trade:
    buy_order_id: int
    sell_order_id: int
    price: int
    quantity: int
    timestamp: datetime = field(default_factory=datetime.now)