from lob.models import Order, Trade


class OrderBook:
    """Holds resting orders and matches incoming ones using price-time priority."""

    def __init__(self):
        # Both lists are kept sorted at all times, so the best order is always at index 0.
        self.bids: list[Order] = []  # buy orders: highest price first, same price -> oldest first
        self.asks: list[Order] = []  # sell orders: lowest price first, same price -> oldest first

    # Looking at the top of the book

    def best_bid(self) -> Order | None:
        """The highest-priced buy order, or None if there are no bids."""
        return self.bids[0] if self.bids else None

    def best_ask(self) -> Order | None:
        """The lowest-priced sell order, or None if there are no asks."""
        return self.asks[0] if self.asks else None

    # Adding an order (the matching engine) 

    def add(self, order: Order) -> list[Trade]:
        """Match an incoming order against the book, rest any leftover, return the trades."""
        trades: list[Trade] = []

        # A buy trades against asks; a sell trades against bids.
        if order.side == "buy":
            opposite = self.asks

            def crosses(resting: Order) -> bool:
                return order.price >= resting.price  # willing to pay at least the ask
        else:
            opposite = self.bids

            def crosses(resting: Order) -> bool:
                return order.price <= resting.price  # willing to sell at or below the bid

        # Keep matching until the order is filled, the other side is empty,
        # or the best price on the other side is too far away.
        while order.quantity > 0 and opposite and crosses(opposite[0]):
            resting = opposite[0]
            qty = min(order.quantity, resting.quantity)

            if order.side == "buy":
                buyer, seller = order, resting
            else:
                buyer, seller = resting, order

            # The trade happens at the resting order's price: it was in the book first.
            trades.append(Trade(buyer.id, seller.id, resting.price, qty))

            order.quantity -= qty
            resting.quantity -= qty
            if resting.quantity == 0:
                opposite.pop(0)  # fully filled, remove it from the book

        # Whatever didn't trade waits in the book.
        if order.quantity > 0:
            self._rest(order)

        return trades

    def _rest(self, order: Order) -> None:
        """Insert an order into its side of the book at the correct sorted position."""
        if order.side == "buy":
            side = self.bids

            def stays_ahead(resting: Order) -> bool:
                return resting.price >= order.price
        else:
            side = self.asks

            def stays_ahead(resting: Order) -> bool:
                return resting.price <= order.price

        # Walk past every order that should stay in front of this one.
        # The "or equal" means an older order at the same price stays ahead (time priority).
        i = 0
        while i < len(side) and stays_ahead(side[i]):
            i += 1
        side.insert(i, order)

    # Cancelling 

    def cancel(self, order_id: int) -> bool:
        """Remove the order with this id. Returns True if found, False if not."""
        for side in (self.bids, self.asks):
            for i, resting in enumerate(side):
                if resting.id == order_id:
                    side.pop(i)
                    return True
        return False