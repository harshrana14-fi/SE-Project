import time
from cart import Cart
from payment import PaymentService
from order import OrderService


def test_end_to_end_amount_correct():
    svc = OrderService(PaymentService())
    c = Cart(); c.add_item(499.50, 2); c.add_item(250.25, 1)   # 1249.25 less 10% = 1124.325 -> 1124.33
    assert svc.checkout(c, discount_percent=10)["paid_paise"] == 112433

def test_load_1000_checkouts_under_3_seconds():
    svc = OrderService(PaymentService())
    start = time.perf_counter()
    for i in range(1000):
        c = Cart(); c.add_item(100 + i, 1)
        assert svc.checkout(c)["status"] == "CONFIRMED"
    assert time.perf_counter() - start < 3
