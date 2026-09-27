from models.account import BankAccount


def format_currency(amount: float) -> str:
    return f"₹{amount:,.2f}"


def print_table(rows: list[dict], columns: list[str]) -> None:
    if not rows:
        print("No records found.")
        return
    widths = {column: max(len(column), *(len(str(row.get(column, ""))) for row in rows)) for column in columns}
    header = " | ".join(column.ljust(widths[column]) for column in columns)
    print(header)
    print("-+-".join("-" * widths[column] for column in columns))
    for row in rows:
        print(" | ".join(str(row.get(column, "")).ljust(widths[column]) for column in columns))


def account_to_dict(account: BankAccount) -> dict:
    return account.get_summary()
