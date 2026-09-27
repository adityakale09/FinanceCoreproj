from datetime import datetime
from models.account import BankAccount, SavingsAccount, CurrentAccount, BusinessAccount
from models.customer import Customer
from models.transaction import Transaction
from services.storage import (
    ACCOUNTS_FILE, CUSTOMERS_FILE, TRANSACTIONS_FILE,
    ACCOUNT_FIELDS, CUSTOMER_FIELDS, TRANSACTION_FIELDS,
    append_row, next_id, read_rows, write_rows,
)

ACCOUNT_CLASSES = {
    "Savings": SavingsAccount,
    "Current": CurrentAccount,
    "Business": BusinessAccount,
}


class BankingService:
    """Application service containing customer, account and transaction operations."""

    def create_customer(self, name: str, email: str, phone: str) -> Customer:
        rows = read_rows(CUSTOMERS_FILE)
        if any(row["email"].lower() == email.lower() for row in rows):
            raise ValueError("A customer with this email already exists.")
        customer = Customer(next_id(CUSTOMERS_FILE, "customer_id"), name, email, phone)
        append_row(CUSTOMERS_FILE, CUSTOMER_FIELDS, customer.summary())
        return customer

    def get_customers(self) -> list[Customer]:
        return [
            Customer(int(r["customer_id"]), r["name"], r["email"], r["phone"])
            for r in read_rows(CUSTOMERS_FILE)
        ]

    def find_customer(self, customer_id: int) -> Customer | None:
        for customer in self.get_customers():
            if customer.customer_id == customer_id:
                return customer
        return None

    def create_account(self, customer_id: int, account_type: str, opening_balance: float = 0.0) -> BankAccount:
        customer = self.find_customer(customer_id)
        if customer is None:
            raise ValueError("Customer not found.")
        if account_type not in ACCOUNT_CLASSES:
            raise ValueError("Account type must be Savings, Current or Business.")
        if opening_balance < 0:
            raise ValueError("Opening balance cannot be negative.")
        account_number = f"FC{customer_id:03d}{next_id(ACCOUNTS_FILE, 'account_number'):05d}"
        # next_id cannot parse alphanumeric account numbers, so use row count for uniqueness.
        rows = read_rows(ACCOUNTS_FILE)
        account_number = f"FC{customer_id:03d}{len(rows) + 1:05d}"
        account_cls = ACCOUNT_CLASSES[account_type]
        account = account_cls(account_number, customer_id, customer.name, opening_balance)
        append_row(ACCOUNTS_FILE, ACCOUNT_FIELDS, {
            "account_number": account.account_number,
            "customer_id": account.customer_id,
            "owner_name": account.owner_name,
            "account_type": account.account_type,
            "balance": account.balance,
        })
        self._update_customer_accounts(customer.customer_id, account.account_number)
        if opening_balance > 0:
            self._record_transaction(account.account_number, "Deposit", opening_balance, "Opening Balance", "Opening account deposit")
        return account

    def get_accounts(self) -> list[BankAccount]:
        accounts = []
        for row in read_rows(ACCOUNTS_FILE):
            cls = ACCOUNT_CLASSES.get(row["account_type"], BankAccount)
            accounts.append(cls(row["account_number"], int(row["customer_id"]), row["owner_name"], float(row["balance"])))
        return accounts

    def find_account(self, account_number: str) -> BankAccount | None:
        for account in self.get_accounts():
            if account.account_number == account_number:
                return account
        return None

    def deposit(self, account_number: str, amount: float, category: str = "Deposit", description: str = "Cash deposit") -> Transaction:
        account = self._require_account(account_number)
        account.deposit(amount)
        self._save_account_balance(account)
        return self._record_transaction(account_number, "Deposit", amount, category, description)

    def withdraw(self, account_number: str, amount: float, category: str = "Withdrawal", description: str = "Cash withdrawal") -> Transaction:
        account = self._require_account(account_number)
        account.withdraw(amount)
        self._save_account_balance(account)
        return self._record_transaction(account_number, "Withdrawal", amount, category, description)

    def transfer(self, source: str, destination: str, amount: float, description: str = "Account transfer") -> tuple[Transaction, Transaction]:
        if source == destination:
            raise ValueError("Source and destination accounts must be different.")
        source_account = self._require_account(source)
        destination_account = self._require_account(destination)
        source_account.withdraw(amount)
        destination_account.deposit(amount)
        self._save_account_balance(source_account)
        self._save_account_balance(destination_account)
        outgoing = self._record_transaction(source, "Transfer Out", amount, "Transfer", description, destination)
        incoming = self._record_transaction(destination, "Transfer In", amount, "Transfer", description, source)
        return outgoing, incoming

    def get_transactions(self) -> list[Transaction]:
        transactions = []
        for row in read_rows(TRANSACTIONS_FILE):
            transactions.append(Transaction(
                int(row["transaction_id"]), row["account_number"], row["transaction_type"],
                float(row["amount"]), row["category"], row["description"],
                row["transaction_date"], row["status"], row.get("related_account", "")
            ))
        return transactions

    def search_transactions(self, keyword: str) -> list[Transaction]:
        keyword = keyword.lower().strip()
        results = []
        for transaction in self.get_transactions():
            searchable = " ".join([
                transaction.account_number, transaction.transaction_type,
                transaction.category, transaction.description
            ]).lower()
            if keyword in searchable:
                results.append(transaction)
        return results

    def _require_account(self, account_number: str) -> BankAccount:
        account = self.find_account(account_number)
        if account is None:
            raise ValueError("Account not found.")
        return account

    def _save_account_balance(self, account: BankAccount) -> None:
        rows = read_rows(ACCOUNTS_FILE)
        for row in rows:
            if row["account_number"] == account.account_number:
                row["balance"] = f"{account.balance:.2f}"
        write_rows(ACCOUNTS_FILE, ACCOUNT_FIELDS, rows)

    def _update_customer_accounts(self, customer_id: int, account_number: str) -> None:
        rows = read_rows(CUSTOMERS_FILE)
        # The CSV stores only core customer fields; account ownership is derived from accounts.csv.
        # The method exists to keep the service boundary explicit.
        for row in rows:
            if int(row["customer_id"]) == customer_id:
                return

    def _record_transaction(self, account_number: str, transaction_type: str, amount: float,
                            category: str, description: str, related_account: str = "") -> Transaction:
        transaction = Transaction(
            transaction_id=next_id(TRANSACTIONS_FILE, "transaction_id"),
            account_number=account_number,
            transaction_type=transaction_type,
            amount=float(amount),
            category=category,
            description=description,
            transaction_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            related_account=related_account,
        )
        append_row(TRANSACTIONS_FILE, TRANSACTION_FIELDS, transaction.to_dict())
        return transaction
