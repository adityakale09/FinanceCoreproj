import os
import numpy as np
import pandas as pd

from services.storage import TRANSACTIONS_FILE


def load_transactions(path: str = TRANSACTIONS_FILE) -> pd.DataFrame:
    if not os.path.exists(path):
        return pd.DataFrame(columns=[
            "transaction_id", "account_number", "transaction_type", "amount",
            "category", "description", "transaction_date", "status", "related_account"
        ])
    df = pd.read_csv(path)
    if not df.empty:
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
        df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
        df["month"] = df["transaction_date"].dt.to_period("M").astype(str)
    return df


def build_summary(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "total_income": 0.0,
            "total_expenses": 0.0,
            "net_change": 0.0,
            "average_transaction": 0.0,
            "largest_transaction": 0.0,
            "transaction_count": 0,
        }
    income_types = {"Deposit", "Transfer In"}
    expense_types = {"Withdrawal", "Transfer Out"}
    income = df.loc[df["transaction_type"].isin(income_types), "amount"]
    expenses = df.loc[df["transaction_type"].isin(expense_types), "amount"]
    return {
        "total_income": round(float(income.sum()), 2),
        "total_expenses": round(float(expenses.sum()), 2),
        "net_change": round(float(income.sum() - expenses.sum()), 2),
        "average_transaction": round(float(np.mean(df["amount"])), 2),
        "largest_transaction": round(float(np.max(df["amount"])), 2),
        "transaction_count": int(len(df)),
    }


def category_expenses(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["category", "amount"])
    expense_types = {"Withdrawal", "Transfer Out"}
    result = (
        df[df["transaction_type"].isin(expense_types)]
        .groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )
    return result


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["month", "income", "expenses", "net_change"])
    income_types = {"Deposit", "Transfer In"}
    expense_types = {"Withdrawal", "Transfer Out"}
    working = df.copy()
    working["income"] = np.where(working["transaction_type"].isin(income_types), working["amount"], 0)
    working["expenses"] = np.where(working["transaction_type"].isin(expense_types), working["amount"], 0)
    result = working.groupby("month", as_index=False)[["income", "expenses"]].sum()
    result["net_change"] = result["income"] - result["expenses"]
    return result.sort_values("month")


def unique_categories(df: pd.DataFrame) -> set[str]:
    if df.empty:
        return set()
    return set(df["category"].dropna().astype(str))


def generate_report(output_path: str = "reports/financial_report.csv") -> str:
    df = load_transactions()
    summary = build_summary(df)
    category = category_expenses(df)
    monthly = monthly_summary(df)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("FINCORE FINANCIAL REPORT\n\n")
        for key, value in summary.items():
            file.write(f"{key}: {value}\n")
        file.write("\nCATEGORY EXPENSES\n")
        if category.empty:
            file.write("No data\n")
        else:
            file.write(category.to_string(index=False))
        file.write("\n\nMONTHLY SUMMARY\n")
        if monthly.empty:
            file.write("No data\n")
        else:
            file.write(monthly.to_string(index=False))
    return output_path
