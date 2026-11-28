import pytest

from lob.models import Order
from lob.order_book import OrderBook


def buy(price, qty):
    return Order("buy", price, qty)


def sell(price, qty):
    return Order("sell", price, qty)


# Milestone 2: resting orders, no matching

def test_empty_book_has_no_best_prices():
    book = OrderBook()
    assert book.best_bid() is None
    assert book.best_ask() is None


def test_bids_sorted_highest_first_asks_lowest_first():
    book = OrderBook()
    book.add(buy(9900, 1))
    book.add(buy(10000, 1))
    book.add(sell(10200, 1))
    book.add(sell(10100, 1))
    assert book.best_bid().price == 10000
    assert book.best_ask().price == 10100


# Milestone 3: matching 

def test_no_cross_means_no_trade():
    book = OrderBook()
    book.add(sell(10100, 5))
    trades = book.add(buy(10000, 5))
    assert trades == []
    assert book.best_bid().price == 10000
    assert book.best_ask().price == 10100


def test_exact_fill_clears_both_sides():
    book = OrderBook()
    s = sell(10000, 5)
    book.add(s)
    b = buy(10000, 5)
    trades = book.add(b)
    assert len(trades) == 1
    t = trades[0]
    assert (t.buy_order_id, t.sell_order_id, t.price, t.quantity) == (b.id, s.id, 10000, 5)
    assert book.best_bid() is None
    assert book.best_ask() is None


def test_trade_happens_at_resting_price():
    book = OrderBook()
    book.add(sell(10000, 5))
    trades = book.add(buy(10500, 5))  # willing to pay more, but gets the ask's price
    assert trades[0].price == 10000


def test_big_incoming_order_rests_remainder():
    book = OrderBook()
    book.add(sell(10000, 3))
    trades = book.add(buy(10000, 10))
    assert trades[0].quantity == 3
    assert book.best_ask() is None
    assert book.best_bid().price == 10000
    assert book.best_bid().quantity == 7


def test_small_incoming_order_leaves_resting_remainder():
    book = OrderBook()
    book.add(sell(10000, 10))
    trades = book.add(buy(10000, 4))
    assert trades[0].quantity == 4
    assert book.best_bid() is None
    assert book.best_ask().quantity == 6


def test_sweeps_multiple_price_levels():
    book = OrderBook()
    book.add(sell(10000, 2))
    book.add(sell(10100, 2))
    book.add(sell(10200, 2))
    trades = book.add(buy(10100, 5))
    assert [(t.price, t.quantity) for t in trades] == [(10000, 2), (10100, 2)]
    assert book.best_bid().quantity == 1      # 1 left over rests at 101.00
    assert book.best_ask().price == 10200     # untouched level remains


def test_time_priority_at_same_price():
    book = OrderBook()
    first = sell(10000, 5)
    second = sell(10000, 5)
    book.add(first)
    book.add(second)
    trades = book.add(buy(10000, 5))
    assert trades[0].sell_order_id == first.id


def test_incoming_sell_matches_bids():
    book = OrderBook()
    b = buy(10000, 5)
    book.add(b)
    s = sell(9900, 5)
    trades = book.add(s)
    assert (trades[0].buy_order_id, trades[0].sell_order_id, trades[0].price) == (b.id, s.id, 10000)


# Milestone 4: cancel 

def test_cancel_removes_order():
    book = OrderBook()
    b = buy(10000, 5)
    book.add(b)
    assert book.cancel(b.id) is True
    assert book.best_bid() is None


def test_cancel_unknown_id_returns_false():
    book = OrderBook()
    assert book.cancel(999) is False


# Milestone 1: model validation 

def test_invalid_orders_rejected():
    with pytest.raises(ValueError):
        Order("hold", 10000, 1)
    with pytest.raises(ValueError):
        Order("buy", 10000, 0)