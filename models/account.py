from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BankAccount:
    """Base class for all bank accounts."""
    account_number: str
    customer_id: int
    owner_name: str
    balance: float = 0.0
    transactions: list = field(default_factory=list)

    account_type = "Bank"
    minimum_balance = 0.0

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self.balance += amount
        return self.balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if self.balance - amount < self.minimum_balance:
            raise ValueError("Withdrawal would violate the minimum balance rule.")
        self.balance -= amount
        return self.balance

    def add_transaction(self, transaction: dict) -> None:
        self.transactions.append(transaction)

    def get_summary(self) -> dict:
        return {
            "account_number": self.account_number,
            "owner_name": self.owner_name,
            "account_type": self.account_type,
            "balance": round(self.balance, 2),
            "transaction_count": len(self.transactions),
        }

    def calculate_interest(self) -> float:
        return 0.0


@dataclass
class SavingsAccount(BankAccount):
    account_type = "Savings"
    minimum_balance = 500.0
    interest_rate = 0.04

    def withdraw(self, amount: float) -> float:
        """Polymorphic withdrawal: savings accounts keep a minimum balance."""
        if amount > 25000:
            raise ValueError("Savings withdrawal limit is ₹25,000 per transaction.")
        return super().withdraw(amount)

    def calculate_interest(self) -> float:
        return round(self.balance * self.interest_rate / 12, 2)


@dataclass
class CurrentAccount(BankAccount):
    account_type = "Current"
    minimum_balance = 0.0
    overdraft_limit = 10000.0

    def withdraw(self, amount: float) -> float:
        """Polymorphic withdrawal: current accounts permit limited overdraft."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if self.balance - amount < -self.overdraft_limit:
            raise ValueError("Overdraft limit exceeded.")
        self.balance -= amount
        return self.balance


@dataclass
class BusinessAccount(CurrentAccount):
    account_type = "Business"
    transaction_fee = 25.0

    def withdraw(self, amount: float) -> float:
        """Polymorphic withdrawal: business account applies a transaction fee."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        total = amount + self.transaction_fee
        if self.balance - total < -self.overdraft_limit:
            raise ValueError("Withdrawal plus business fee exceeds overdraft limit.")
        self.balance -= total
        return self.balance

    def calculate_interest(self) -> float:
        return 0.0
