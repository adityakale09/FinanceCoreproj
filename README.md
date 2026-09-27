# FinCore — Personal Banking & Financial Analytics System

FinCore is a Python-only educational banking simulation designed around 12 core Python practical objectives. It demonstrates procedural programming, data structures, modular programming, OOP, inheritance, polymorphism, and Pandas/NumPy data manipulation in one coherent application.

> This is an educational simulation. It does not connect to real banks or payment systems.

## Requirements

- Python 3.10+
- Any Python IDE (VS Code, PyCharm, IDLE, etc.)
- Pandas
- NumPy

## Installation

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run with demo data

```bash
python seed_demo.py
python main.py
```

Demo data is fictional. Running `seed_demo.py` resets the CSV files to the included demo dataset.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Main features

- Customer creation
- Savings, Current and Business accounts
- Deposits
- Withdrawals
- Transfers
- Transaction history
- Transaction search
- Financial summaries
- Category-wise expense analysis
- Monthly income/expense analysis
- CSV report generation

## Python practical mapping

| Practical | Demonstration in FinCore |
|---|---|
| 01 | Python setup, virtual environment, interactive execution and running `main.py` |
| 02 | Variables, identifiers, keywords and constants across modules |
| 03 | Arithmetic, comparison, logical and assignment operators in banking rules and analytics |
| 04 | `if/elif/else` for validation, account rules and menu decisions |
| 05 | `for` and `while` loops for menu control and record processing |
| 06 | `break`, `continue` and `pass` in menu/input control flow |
| 07 | Lists and tuples for transaction/account collections and fixed account types |
| 08 | Sets and dictionaries for categories, summaries and structured records |
| 09 | User-defined functions and custom modules under `models/`, `services/`, `utils/` and `analytics/` |
| 10 | `Customer`, `Transaction`, `BankAccount` and other classes/objects |
| 11 | `SavingsAccount`, `CurrentAccount` and `BusinessAccount` inherit from `BankAccount`; overridden methods demonstrate polymorphism |
| 12 | Pandas DataFrames/groupby/filtering and NumPy numerical operations in `analytics/financial_analysis.py` |

See `docs/practical_mapping.md` for a more detailed mapping.
