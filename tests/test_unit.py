import pytest
from unittest.mock import Mock
from decimal import Decimal
from cart import Cart
from order import OrderService


def test_total_with_discount():
    c = Cart(); c.add_item(500.00, 2)
    assert c.total(10) == Decimal("900.00")

def test_total_without_discount():
    c = Cart(); c.add_item(199.99, 1)
    assert c.total() == Decimal("199.99")

def test_negative_quantity_rejected():
    with pytest.raises(ValueError):
        Cart().add_item(100.00, -1)

def test_negative_price_rejected():
    with pytest.raises(ValueError):
        Cart().add_item(-5, 1)

@pytest.mark.parametrize("d", [-1, 101])
def test_discount_boundaries_rejected(d):
    c = Cart(); c.add_item(100, 1)
    with pytest.raises(ValueError):
        c.total(d)

@pytest.mark.parametrize("d,exp", [(0, "100.00"), (100, "0.00")])
def test_discount_boundaries_accepted(d, exp):
    c = Cart(); c.add_item(100, 1)
    assert c.total(d) == Decimal(exp)

def test_checkout_empty_cart_rejected():
    with pytest.raises(ValueError):
        OrderService(Mock()).checkout(Cart())

def test_checkout_with_mocked_payment():
    pay = Mock(); pay.charge.return_value = Mock(status="SUCCESS", amount_paise=5000)
    c = Cart(); c.add_item(50, 1)
    assert OrderService(pay).checkout(c)["status"] == "CONFIRMED"
