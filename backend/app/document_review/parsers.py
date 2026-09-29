import re
from datetime import date
from decimal import Decimal, InvalidOperation

from dateutil import parser


def parse_date(value: str) -> date | None:
    if not value.strip():
        return None
    try:
        return parser.parse(value.strip(), dayfirst=True).date()
    except Exception:
        return None


def parse_integer_decimal(value: str) -> Decimal | None:
    digits_only = re.sub(r"\D", "", str(value))
    if not digits_only:
        return None
        
    try:
        return Decimal(digits_only)
    except InvalidOperation:
        return None


def parse_string(value: str) -> str | None:
    clean = value.strip()
    return clean if clean else None