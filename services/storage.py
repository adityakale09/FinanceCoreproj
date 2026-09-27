import csv
import os
from typing import Iterable

CUSTOMERS_FILE = os.path.join("data", "customers.csv")
ACCOUNTS_FILE = os.path.join("data", "accounts.csv")
TRANSACTIONS_FILE = os.path.join("data", "transactions.csv")

CUSTOMER_FIELDS = ["customer_id", "name", "email", "phone"]
ACCOUNT_FIELDS = ["account_number", "customer_id", "owner_name", "account_type", "balance"]
TRANSACTION_FIELDS = [
    "transaction_id", "account_number", "transaction_type", "amount", "category",
    "description", "transaction_date", "status", "related_account"
]


def ensure_data_directory() -> None:
    os.makedirs("data", exist_ok=True)
    os.makedirs("reports", exist_ok=True)


def ensure_file(path: str, fieldnames: list[str]) -> None:
    ensure_data_directory()
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as file:
            csv.DictWriter(file, fieldnames=fieldnames).writeheader()


def append_row(path: str, fieldnames: list[str], row: dict) -> None:
    ensure_file(path, fieldnames)
    with open(path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_rows(path: str) -> list[dict]:
    ensure_file(path, [])
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_rows(path: str, fieldnames: list[str], rows: Iterable[dict]) -> None:
    ensure_data_directory()
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def next_id(path: str, key: str) -> int:
    rows = read_rows(path)
    values = []
    for row in rows:
        try:
            values.append(int(row[key]))
        except (KeyError, TypeError, ValueError):
            continue
    return max(values, default=0) + 1
