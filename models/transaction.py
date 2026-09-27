from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    transaction_id: int
    account_number: str
    transaction_type: str
    amount: float
    category: str
    description: str
    transaction_date: str
    status: str = "Completed"
    related_account: str = ""

    def to_dict(self) -> dict:
        return {
            "transaction_id": self.transaction_id,
            "account_number": self.account_number,
            "transaction_type": self.transaction_type,
            "amount": round(float(self.amount), 2),
            "category": self.category,
            "description": self.description,
            "transaction_date": self.transaction_date,
            "status": self.status,
            "related_account": self.related_account,
        }
