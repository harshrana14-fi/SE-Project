"""FIRST VERSION of Payment (contains an interface defect found by integration testing)."""
from dataclasses import dataclass


@dataclass
class Receipt:
    amount_paise: int
    status: str


class PaymentService:
    def charge(self, amount, card_valid=True):
        if not card_valid:
            return Receipt(0, "DECLINED")
        return Receipt(int(float(amount) * 100), "SUCCESS")   # DEFECT: float truncation
