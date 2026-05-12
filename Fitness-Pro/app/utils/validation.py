import re


def is_email(value):
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value or ""))


def required_fields(form, fields):
    missing = [field for field in fields if not str(form.get(field, "")).strip()]
    return missing


def parse_float(value, default=None):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_int(value, default=None):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
