from dataclasses import dataclass, field
from typing import List


@dataclass
class Customer:
    customer_id: int
    name: str
    email: str
    phone: str
    accounts: List[str] = field(default_factory=list)

    def add_account(self, account_number: str) -> None:
        if account_number not in self.accounts:
            self.accounts.append(account_number)

    def summary(self) -> dict:
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "account_count": len(self.accounts),
        }
