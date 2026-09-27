"""FinCore - Personal Banking & Financial Analytics System.

Python-only educational project designed to demonstrate 12 core Python practicals.
"""

from analytics.financial_analysis import (
    build_summary, category_expenses, generate_report, load_transactions, monthly_summary,
)
from services.banking import BankingService
from services.storage import ensure_data_directory
from utils.helpers import format_currency, print_table
from utils.validators import positive_amount, validate_email, validate_name, valid_choice


class FinCoreApp:
    def __init__(self):
        ensure_data_directory()
        self.bank = BankingService()

    def run(self):
        print("\n" + "=" * 58)
        print("        FINCORE - BANKING & ANALYTICS SYSTEM")
        print("=" * 58)
        while True:
            self.show_menu()
            choice = input("Enter choice: ").strip()
            if choice == "0":
                print("Thank you for using FinCore.")
                break
            if not choice.isdigit():
                print("Invalid choice. Please enter a number.")
                continue
            if choice == "1":
                self.create_customer()
            elif choice == "2":
                self.create_account()
            elif choice == "3":
                self.deposit()
            elif choice == "4":
                self.withdraw()
            elif choice == "5":
                self.transfer()
            elif choice == "6":
                self.show_accounts()
            elif choice == "7":
                self.show_transactions()
            elif choice == "8":
                self.search_transactions()
            elif choice == "9":
                self.analytics()
            elif choice == "10":
                self.generate_report()
            elif choice == "11":
                self.show_practical_mapping()
            else:
                # pass is intentionally used for an unsupported menu branch.
                pass
                print("Unknown option. Please choose a valid menu item.")

    @staticmethod
    def show_menu():
        print("""
1. Create Customer
2. Create Bank Account
3. Deposit Money
4. Withdraw Money
5. Transfer Money
6. View Accounts
7. View Transaction History
8. Search Transactions
9. Financial Analytics
10. Generate Financial Report
11. View Practical Mapping
0. Exit
""")

    def create_customer(self):
        try:
            name = validate_name(input("Name: "))
            email = validate_email(input("Email: "))
            phone = input("Phone: ").strip()
            customer = self.bank.create_customer(name, email, phone)
            print(f"Customer created successfully. ID: {customer.customer_id}")
        except ValueError as exc:
            print(f"Error: {exc}")

    def create_account(self):
        try:
            customer_id = int(input("Customer ID: "))
            account_type = valid_choice(input("Account type (Savings/Current/Business): "), {"Savings", "Current", "Business"})
            opening_text = input("Opening balance (0 for none): ").strip()
            opening_balance = 0.0 if opening_text == "0" else positive_amount(opening_text)
            account = self.bank.create_account(customer_id, account_type, opening_balance)
            print(f"Account created: {account.account_number}")
        except ValueError as exc:
            print(f"Error: {exc}")

    def deposit(self):
        try:
            account = input("Account number: ").strip()
            amount = positive_amount(input("Amount: "))
            category = input("Category [default Deposit]: ").strip() or "Deposit"
            description = input("Description [default Cash deposit]: ").strip() or "Cash deposit"
            tx = self.bank.deposit(account, amount, category, description)
            print(f"Deposit successful. Transaction #{tx.transaction_id}")
        except ValueError as exc:
            print(f"Error: {exc}")

    def withdraw(self):
        try:
            account = input("Account number: ").strip()
            amount = positive_amount(input("Amount: "))
            category = input("Category [default Withdrawal]: ").strip() or "Withdrawal"
            description = input("Description [default Cash withdrawal]: ").strip() or "Cash withdrawal"
            tx = self.bank.withdraw(account, amount, category, description)
            print(f"Withdrawal successful. Transaction #{tx.transaction_id}")
        except ValueError as exc:
            print(f"Error: {exc}")

    def transfer(self):
        try:
            source = input("Source account: ").strip()
            destination = input("Destination account: ").strip()
            amount = positive_amount(input("Amount: "))
            description = input("Description [default Account transfer]: ").strip() or "Account transfer"
            outgoing, _ = self.bank.transfer(source, destination, amount, description)
            print(f"Transfer successful. Transaction #{outgoing.transaction_id}")
        except ValueError as exc:
            print(f"Error: {exc}")

    def show_accounts(self):
        accounts = self.bank.get_accounts()
        rows = []
        for account in accounts:  # Practical 05: for loop
            summary = account.get_summary()
            rows.append({
                "Account": summary["account_number"],
                "Owner": summary["owner_name"],
                "Type": summary["account_type"],
                "Balance": format_currency(summary["balance"]),
            })
        print_table(rows, ["Account", "Owner", "Type", "Balance"])

    def show_transactions(self):
        transactions = self.bank.get_transactions()
        rows = []
        for tx in transactions:
            rows.append({
                "ID": tx.transaction_id,
                "Account": tx.account_number,
                "Type": tx.transaction_type,
                "Amount": format_currency(tx.amount),
                "Category": tx.category,
                "Date": tx.transaction_date,
            })
        print_table(rows, ["ID", "Account", "Type", "Amount", "Category", "Date"])

    def search_transactions(self):
        keyword = input("Search keyword: ").strip()
        results = self.bank.search_transactions(keyword)
        rows = [{
            "ID": tx.transaction_id,
            "Account": tx.account_number,
            "Type": tx.transaction_type,
            "Amount": format_currency(tx.amount),
            "Category": tx.category,
        } for tx in results]
        print_table(rows, ["ID", "Account", "Type", "Amount", "Category"])

    def analytics(self):
        df = load_transactions()
        summary = build_summary(df)
        print("\n========== FINANCIAL ANALYTICS ==========")
        print(f"Total income       : {format_currency(summary['total_income'])}")
        print(f"Total expenses     : {format_currency(summary['total_expenses'])}")
        print(f"Net change         : {format_currency(summary['net_change'])}")
        print(f"Average transaction: {format_currency(summary['average_transaction'])}")
        print(f"Largest transaction: {format_currency(summary['largest_transaction'])}")
        print(f"Transaction count  : {summary['transaction_count']}")

        categories = category_expenses(df)
        print("\n----- EXPENSE BY CATEGORY -----")
        if categories.empty:
            print("No expense data.")
        else:
            print(categories.to_string(index=False))

        monthly = monthly_summary(df)
        print("\n----- MONTHLY SUMMARY -----")
        if monthly.empty:
            print("No monthly data.")
        else:
            print(monthly.to_string(index=False))

        # Practical 08: set operation on unique categories.
        unique_category_names = set(df["category"].dropna().astype(str)) if not df.empty else set()
        print(f"\nUnique categories ({len(unique_category_names)}): {sorted(unique_category_names)}")

    @staticmethod
    def generate_report():
        path = generate_report()
        print(f"Report generated successfully: {path}")

    @staticmethod
    def show_practical_mapping():
        print("""
========== 12 PYTHON PRACTICALS MAPPING ==========
01  Python setup and execution      -> Project setup + main.py execution
02  Variables/identifiers/keywords  -> All Python modules
03  Operators                       -> Banking calculations and validations
04  Conditional statements          -> Account and transaction rules
05  for/while loops                 -> Menu, transactions and report processing
06  break/continue/pass             -> Menu and validation control flow
07  lists/tuples                    -> Transactions, account types and collections
08  sets/dictionaries                -> Categories, records and analytics summaries
09  functions/modules               -> services/, models/, utils/, analytics/
10  classes/objects                 -> Customer, Transaction, BankAccount
11  inheritance/polymorphism        -> Savings/Current/Business account classes
12  data manipulation library       -> Pandas + NumPy analytics
""")


if __name__ == "__main__":
    FinCoreApp().run()
