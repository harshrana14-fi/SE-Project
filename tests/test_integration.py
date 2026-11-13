import importlib
from cart import Cart
from order import OrderService


def _payment(module):
    return importlib.import_module(module).PaymentService()

def test_cart_amount_reaches_payment_v1():
    """Run against the FIRST version of Payment (expected to expose the defect)."""
    c = Cart(); c.add_item(4.35, 1)
    receipt = _payment("payment_v1").charge(c.total())
    assert receipt.amount_paise == 435

def test_cart_amount_reaches_payment():
    c = Cart(); c.add_item(199.99, 1)
    assert _payment("payment").charge(c.total()).amount_paise == 19999

def test_odd_amounts_no_rounding_loss():
    for price in (0.07, 0.29, 1.15, 19.99, 4.35, 1234.56):
        c = Cart(); c.add_item(price, 1)
        assert _payment("payment").charge(c.total()).amount_paise == round(price * 100)

def test_declined_payment_keeps_cart():
    c = Cart(); c.add_item(100, 2)
    r = OrderService(_payment("payment")).checkout(c, card_valid=False)
    assert r == {"status": "FAILED", "cart_kept": True} and not c.is_empty()

def test_successful_payment_clears_cart():
    c = Cart(); c.add_item(100, 2)
    OrderService(_payment("payment")).checkout(c)
    assert c.is_empty()

def test_zero_amount_rejected():
    import pytest
    with pytest.raises(ValueError):
        _payment("payment").charge(0)
