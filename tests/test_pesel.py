import pytest
from datetime import date

from pesel import validate_pesel
from exceptions import ValidationError

# POPRAWNE PESELE (checksum + data + płeć):
# 1999-01-05, M
PESEL_OK_M_1999_01_05 = "99010501230"
# 1999-01-05, K
PESEL_OK_K_1999_01_05 = "99010501247"
# 2003-12-31, K (miesiąc kodowany: 12 + 20 = 32)
PESEL_OK_K_2003_12_31 = "03323100082"
# 1888-02-29, M (miesiąc kodowany: 2 + 80 = 82)
PESEL_OK_M_1888_02_29 = "88822901112"


def test_validate_pesel_ok_male_1999():
    info = validate_pesel(PESEL_OK_M_1999_01_05, "M")
    assert info.gender == "M"
    assert info.birth_date == date(1999,1,5)

def test_validate_pesel_ok_female_1999():
    info = validate_pesel(PESEL_OK_K_1999_01_05, "K")
    assert info.gender == "K"
    assert info.birth_date == date(1999, 1,5)

def test_validate_pesel_ok_century_2000s():
    info = validate_pesel(PESEL_OK_K_2003_12_31, "K")
    assert info.birth_date == date(2003,12,31)
    assert info.gender == "K"

def test_validate_pesel_ok_century_1800s_leap_day():
    info = validate_pesel(PESEL_OK_M_1888_02_29, "M")
    assert info.birth_date == date(1888, 2, 29)
    assert info.gender == "M"

def test_invalid_lenght():
    with pytest.raises(ValidationError):
        validate_pesel("123", "M")

def test_invalid_non_digit():
    with pytest.raises(ValidationError):
        validate_pesel("9901050123A", "M")

def test_invalid_check_sum():
    with pytest.raises(ValidationError):
        validate_pesel("99010501231", "M")
    
def test_invalid_date_encoded():
    with pytest.raises(ValidationError):
        validate_pesel("99133200000", "K")

def test_gendeer_mismatch():
    with pytest.raises(ValidationError):
        validate_pesel(PESEL_OK_M_1999_01_05, "K")