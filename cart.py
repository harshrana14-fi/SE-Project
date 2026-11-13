"""Cart module: stores items and calculates the payable total."""
from decimal import Decimal, ROUND_HALF_UP


class Cart:
    def __init__(self):
        self.items = []  # list of (price, qty)

    def add_item(self, price, qty):
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.items.append((Decimal(str(price)), qty))

    def total(self, discount_percent=0):
        if not 0 <= discount_percent <= 100:
            raise ValueError("Discount must be between 0 and 100")
        gross = sum(p * q for p, q in self.items)
        net = gross * (Decimal(100) - Decimal(str(discount_percent))) / Decimal(100)
        return net.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def is_empty(self):
        return not self.items
