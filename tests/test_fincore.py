import os
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from models.account import SavingsAccount, CurrentAccount, BusinessAccount
from analytics.financial_analysis import build_summary, category_expenses, monthly_summary


class TestAccounts(unittest.TestCase):
    def test_savings_minimum_balance(self):
        account = SavingsAccount("S1", 1, "Test", 1000)
        account.withdraw(400)
        self.assertEqual(account.balance, 600)
        with self.assertRaises(ValueError):
            account.withdraw(200)

    def test_current_overdraft(self):
        account = CurrentAccount("C1", 1, "Test", 100)
        account.withdraw(500)
        self.assertEqual(account.balance, -400)
        with self.assertRaises(ValueError):
            account.withdraw(10000)

    def test_business_polymorphic_fee(self):
        account = BusinessAccount("B1", 1, "Test", 1000)
        account.withdraw(100)
        self.assertEqual(account.balance, 875)


class TestAnalytics(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame([
            {"transaction_type": "Deposit", "amount": 1000, "category": "Salary", "month": "2026-09"},
            {"transaction_type": "Withdrawal", "amount": 200, "category": "Food", "month": "2026-09"},
            {"transaction_type": "Withdrawal", "amount": 100, "category": "Bills", "month": "2026-09"},
            {"transaction_type": "Transfer In", "amount": 300, "category": "Transfer", "month": "2026-10"},
        ])

    def test_summary(self):
        summary = build_summary(self.df)
        self.assertEqual(summary["total_income"], 1300)
        self.assertEqual(summary["total_expenses"], 300)
        self.assertEqual(summary["net_change"], 1000)
        self.assertEqual(summary["transaction_count"], 4)

    def test_category_grouping(self):
        result = category_expenses(self.df)
        self.assertEqual(result.iloc[0]["category"], "Food")
        self.assertEqual(result.iloc[0]["amount"], 200)

    def test_monthly_summary(self):
        result = monthly_summary(self.df)
        row = result[result["month"] == "2026-09"].iloc[0]
        self.assertEqual(row["income"], 1000)
        self.assertEqual(row["expenses"], 300)
        self.assertEqual(row["net_change"], 700)


if __name__ == "__main__":
    unittest.main()
