# accounts/utils.py

def normalize_username(value: str) -> str:
    return value.strip()

def normalize_email(value: str) -> str:
    return value.strip().lower()
