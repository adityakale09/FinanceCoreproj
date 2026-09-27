"""Create a small fictional dataset for demonstration and testing."""
import os
from services.storage import (
    ensure_data_directory, write_rows, CUSTOMER_FIELDS, ACCOUNT_FIELDS,
    TRANSACTION_FIELDS, CUSTOMERS_FILE, ACCOUNTS_FILE, TRANSACTIONS_FILE,
)


def seed():
    ensure_data_directory()
    write_rows(CUSTOMERS_FILE, CUSTOMER_FIELDS, [
        {"customer_id": 1, "name": "Aarav Sharma", "email": "aarav@example.com", "phone": "9000000001"},
        {"customer_id": 2, "name": "Priya Patil", "email": "priya@example.com", "phone": "9000000002"},
    ])
    write_rows(ACCOUNTS_FILE, ACCOUNT_FIELDS, [
        {"account_number": "FC00100001", "customer_id": 1, "owner_name": "Aarav Sharma", "account_type": "Savings", "balance": "48500.00"},
        {"account_number": "FC00200002", "customer_id": 2, "owner_name": "Priya Patil", "account_type": "Current", "balance": "27500.00"},
    ])
    write_rows(TRANSACTIONS_FILE, TRANSACTION_FIELDS, [
        {"transaction_id": 1, "account_number": "FC00100001", "transaction_type": "Deposit", "amount": "50000", "category": "Salary", "description": "Monthly salary", "transaction_date": "2026-09-01 09:00:00", "status": "Completed", "related_account": ""},
        {"transaction_id": 2, "account_number": "FC00100001", "transaction_type": "Withdrawal", "amount": "3500", "category": "Food", "description": "Groceries", "transaction_date": "2026-09-03 12:00:00", "status": "Completed", "related_account": ""},
        {"transaction_id": 3, "account_number": "FC00100001", "transaction_type": "Withdrawal", "amount": "8000", "category": "Bills", "description": "Monthly bills", "transaction_date": "2026-09-05 12:00:00", "status": "Completed", "related_account": ""},
        {"transaction_id": 4, "account_number": "FC00100001", "transaction_type": "Withdrawal", "amount": "5000", "category": "Travel", "description": "Travel expense", "transaction_date": "2026-09-10 12:00:00", "status": "Completed", "related_account": ""},
        {"transaction_id": 5, "account_number": "FC00200002", "transaction_type": "Deposit", "amount": "30000", "category": "Business Income", "description": "Client payment", "transaction_date": "2026-09-02 10:00:00", "status": "Completed", "related_account": ""},
        {"transaction_id": 6, "account_number": "FC00200002", "transaction_type": "Withdrawal", "amount": "2500", "category": "Supplies", "description": "Office supplies", "transaction_date": "2026-09-07 14:00:00", "status": "Completed", "related_account": ""},
    ])
    print("Demo data created successfully.")


if __name__ == "__main__":
    seed()
