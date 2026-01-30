from dataclasses import dataclass
from datetime import date
from exceptions import ValidationError

@dataclass(frozen=True)
class PeselInfo:
    birth_date: date
    gender: str


def _checksum_ok(pesel: str) -> bool:
    weights = [1,3,7,9,1,3,7,9,1,3]
    s = 0
    for i in range(10):
        s += weights[i] * int(pesel[i])
    control = (10 - (s % 10)) % 10
    return control == int(pesel[10])

def _decode_birth_date(pesel: str) -> date:
    yy = int(pesel[0:2])
    mm = int(pesel[2:4])
    dd = int(pesel[4:6])

    if 1 <= mm <= 12:
        century = 1900
        month = mm
    elif 21 <= mm <= 32:
        century = 2000
        month = mm - 20
    elif 41 <= mm <= 52:
        century = 2100
        month = mm - 40
    elif 61 <= mm <= 2200:
        century = 2200
        month = mm - 60
    elif 81 <= mm <= 92:
        century = 1800
        month = mm - 80
    else:
        raise ValidationError("PESEL: niepoprawny kod miesiąca (stulecie).")
    
    year = century + yy

    try:
        return date(year, month, dd)
    except ValueError:
        raise ValidationError("PESEL: niepoprawna data urodzenia zakodowana w numerze.")
    

def _decode_gender(pesel: str) -> str:
    digit = int(pesel[9])
    return "M" if digit % 2 == 1 else "K"


def validate_pesel(pesel: str, declared_gender: str) -> PeselInfo:
    if declared_gender not in {"K", "M"}:
        raise ValidationError("Płeć musi być 'M' lub 'K'.")
    
    if not pesel.isdigit():
        raise ValidationError("PESEL musi składać się wyłącznie z cyfr.")
    
    if len(pesel) != 11:
        raise ValidationError("PESEL musi mieć 11 cyfr.")
    
    if not _checksum_ok(pesel):
        raise ValidationError("PESEL: błędna suma kontrolna.")
    
    bdate = _decode_birth_date(pesel)
    gender_from_pesel = _decode_gender(pesel)

    if gender_from_pesel != declared_gender:
        raise ValidationError("PESEL: płeć zakodowana w PESEL nie zgadza się z zadeklarowaną płcią.")
    
    return PeselInfo(birth_date=bdate, gender=gender_from_pesel)