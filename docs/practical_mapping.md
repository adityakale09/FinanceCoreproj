# Detailed Mapping to the 12 Python Practicals

## 01 — Python installation, IDE and interactive mode
The project is executed with Python from any Python IDE or terminal. The README documents virtual-environment setup, package installation and execution. Basic interactive commands can be demonstrated in the Python REPL before running the application.

## 02 — Identifiers, keywords and variables
The project uses Python identifiers such as `customer_id`, `account_number`, `transaction_type`, classes, functions and modules. Python keywords including `class`, `def`, `if`, `for`, `while`, `return`, `import`, `from`, `try`, `except` and `raise` occur naturally throughout the code.

## 03 — Operators
Arithmetic operators are used for balances, fees, interest and analytics. Comparison and logical operators are used for validation and account rules. Assignment operators update state and calculated values.

## 04 — Conditional statements
The application uses `if`, `elif` and `else` for menu decisions, validation, account-type rules, insufficient funds and analytics handling.

## 05 — Iteration
`while` drives the interactive menu. `for` loops process accounts, customers and transactions and build reports.

## 06 — Loop manipulation
`break` exits the main menu. `continue` handles invalid menu input. `pass` is present in the unsupported menu branch and is documented as an example of a no-op loop/control branch.

## 07 — Lists and tuples
Lists store collections such as transactions and accounts. Tuples store fixed account-type choices. List operations include append, iteration, sorting/filtering and slicing-style collection handling.

## 08 — Sets and dictionaries
Sets are used for unique transaction categories. Dictionaries represent structured customer/account/transaction data and analytics summaries.

## 09 — Functions and custom modules
The project is split into custom packages: `models`, `services`, `analytics` and `utils`. Each contains user-defined functions and classes with clear responsibilities.

## 10 — Classes and objects
`Customer`, `Transaction`, `BankAccount`, `SavingsAccount`, `CurrentAccount` and `BusinessAccount` are classes. Runtime instances of these classes are the application's objects.

## 11 — Inheritance and polymorphism
`SavingsAccount`, `CurrentAccount` and `BusinessAccount` inherit from `BankAccount`. Their `withdraw()` and `calculate_interest()` implementations provide polymorphic behavior appropriate to each account type.

## 12 — Data manipulation library
Pandas loads transaction CSV data into DataFrames and performs filtering, grouping, aggregation and date manipulation. NumPy performs numerical calculations and conditional vectorized operations.
