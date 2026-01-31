import pytest
from exceptions import ValidationError
from validators import validate_gender, validate_index_number

def test_validate_gender_ok():
    assert validate_gender("m") == "M"
    assert validate_gender("k") == "K"


def test_validate_gendeer_not_ok():
    with pytest.raises(ValidationError):
        validate_gender("X")


def test_validate_index_number_ok():
    assert validate_index_number("S-0001") == "S-0001"


def test_validate_index_number_not_ok():
    with pytest.raises(ValidationError):
        validate_index_number("!!")