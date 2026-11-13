"""Order module: connects Cart and Payment (checkout workflow)."""


class OrderService:
    def __init__(self, payment):
        self.payment = payment
        self.orders = []

    def checkout(self, cart, discount_percent=0, card_valid=True):
        if cart.is_empty():
            raise ValueError("Cart is empty")
        receipt = self.payment.charge(cart.total(discount_percent), card_valid)
        if receipt.status != "SUCCESS":
            return {"status": "FAILED", "cart_kept": True}
        self.orders.append(receipt)
        cart.items.clear()
        return {"status": "CONFIRMED", "paid_paise": receipt.amount_paise}
