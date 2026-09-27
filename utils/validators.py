import re


def validate_name(name: str) -> str:
    name = name.strip()
    if not name:
        raise ValueError("Name cannot be empty.")
    if not re.fullmatch(r"[A-Za-z][A-Za-z .'-]{1,49}", name):
        raise ValueError("Name contains invalid characters.")
    return name


def validate_email(email: str) -> str:
    email = email.strip().lower()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ValueError("Enter a valid email address.")
    return email


def positive_amount(value: str) -> float:
    try:
        amount = float(value)
    except ValueError as exc:
        raise ValueError("Amount must be numeric.") from exc
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(amount, 2)


def valid_choice(value: str, allowed: set[str]) -> str:
    value = value.strip()
    if value not in allowed:
        raise ValueError(f"Choose one of: {', '.join(sorted(allowed))}")
    return value
