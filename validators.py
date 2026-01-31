import re
from exceptions import ValidationError

NAME_RE = re.compile(r"^[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż\- ]{2,50}$")
INDEX_RE = re.compile(r"^[A-Za-z0-9\-]{3,20}$")


def validate_non_empty(value: str, field_name: str) -> str:
    v = value.strip()
    if not v:
        raise ValidationError(f"{field_name}: pole nie może być puste.")
    return v


def validate_name(value: str, field_name: str) -> str:
    v = validate_non_empty(value, field_name)
    if not NAME_RE.match(v):
        raise ValidationError(
            f"{field_name}: niepoprawny format (2-50 znaków, litery/spacje/myślnik)."
        )
    return v


def validate_address(value: str) -> str:
    v = validate_non_empty(value, "Adres")
    if len(v) < 5:
        raise ValidationError("Adres: zbyt krótki.")
    return v


def validate_index_number(value: str) -> str:
    v = validate_non_empty(value, "Numer indeksu")
    if not INDEX_RE.match(v):
        raise ValidationError("Numer indeksu: dozwolone litery/cyfry/myślnik (3-20 znaków).")
    return v


def validate_gender(value: str) -> str:
    v = validate_non_empty(value, "Płeć").upper()
    if v not in {"M", "K"}:
        raise ValidationError("Płeć musi być 'M' albo 'K'.")
    return v


def validate_pesel_format(value: str) -> str:
    v = validate_non_empty(value, "PESEL")
    if not v.isdigit():
        raise ValidationError("PESEL musi składać się wyłącznie z cyfr.")
    if len(v) != 11:
        raise ValidationError("PESEL musi mieć długość 11 cyfr.")
    return v
