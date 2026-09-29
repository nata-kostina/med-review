from decimal import Decimal

from app.schemas.common import parse_string_field
from app.schemas.document.mapping import parse_number_field


def test_parse_number_field_none():
    assert parse_number_field(None) is None


def test_parse_number_field_content_none():
    field = {"content": None, "confidence": 0.9}
    result = parse_number_field(field)

    assert result is not None
    assert result.value is None
    assert result.content is None
    assert result.confidence == 0.9


def test_parse_number_field_valid_value():
    field = {"content": "42.5", "confidence": 0.95}
    result = parse_number_field(field)

    assert result is not None
    assert result.value == Decimal("42.5")
    assert result.content == "42.5"
    assert result.confidence == 0.95


def test_parse_number_field_without_confidence():
    field = {"content": "100"}
    result = parse_number_field(field)

    assert result is not None
    assert result.value == Decimal("100")
    assert result.content == "100"
    assert result.confidence is None


def test_parse_number_field_empty_payload():
    field = {"content": None, "confidence": None}
    result = parse_number_field(field)

    assert result is not None
    assert result.value is None
    assert result.content is None
    assert result.confidence is None
    
def test_parse_string_field_provided():
    field = {"content": "Patient reports mild fatigue", "confidence": 0.98}
    result = parse_string_field(field)

    assert result is not None
    assert result.value == "Patient reports mild fatigue"
    assert result.content == "Patient reports mild fatigue"
    assert result.confidence == 0.98


def test_parse_string_field_not_provided():
    result = parse_string_field(None)
    assert result is None