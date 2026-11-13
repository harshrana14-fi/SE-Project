"""Payment module (fixed version): converts rupees (Decimal) to paise exactly."""
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Receipt:
    amount_paise: int
    status: str


class PaymentService:
    def charge(self, amount, card_valid=True):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if not card_valid:
            return Receipt(0, "DECLINED")
        return Receipt(int(Decimal(str(amount)) * 100), "SUCCESS")
