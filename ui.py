from models import Student
from exceptions import ValidationError
from validators import (
    validate_name,
    validate_address,
    validate_index_number,
    validate_pesel_format,
    validate_gender,
)
from pesel import validate_pesel


def print_menu() -> None:
    print("\n=== Akademicka baza studentów===")
    print("1) Dodaj studenta")
    print("2) Wyświetl wszystkich")
    print("3) Wyszukaj po nazwisku")
    print("4) Wyszukaj po PESEL")
    print("5) Sortuj po PESEL")
    print("6) Sortuj po nazwisku")
    print("7) Usuń po numerze indeksu")
    print("8) Aktualiuj dane studenta")
    print("9) Zapisz do pliku")
    print("0) Zapisz i wyjdź")


def prompt_until_valid(prompt: str, validator):
    while True:
        raw = input(prompt)
        try:
            return validator(raw)
        except ValidationError as e:
            print(f"[BŁAD] {e}")


def prompt_optional(prompt: str, validator):
    raw = input(prompt).strip()
    if not raw:
        return None
    while True:
        try:
            return validator(raw)
        except ValidationError as e:
            print(f"[BŁĄD] {e}")
            raw = input(prompt).strip()
            if not raw:
                return None

def read_student() -> Student:
    first_name = prompt_until_valid(validate_name(input("Imię: "), "Imię"))
    last_name = prompt_until_valid(validate_name(input("Nazwisko: "), "Nazwisko"))
    address = prompt_until_valid(validate_address(input("Adres: ")))
    index_number = prompt_until_valid(validate_index_number(input("Numer indeksu: ")))
    pesel = prompt_until_valid(validate_pesel_format(input("PESEL (11 cyfr): ")))
    gender = prompt_until_valid(validate_gender(input("Płeć (M/K): ")))

    return Student(
        first_name=first_name,
        last_name=last_name,
        address=address,
        index_number=index_number,
        pesel=pesel,
        gender=gender,
    )


def read_student_with_pesel_validation() -> Student:
    first_name = prompt_until_valid("Imię: ", lambda v: validate_name(v, "Imię"))
    last_name = prompt_until_valid("Nazwisko: ", lambda v: validate_name(v, "Nazwisko"))
    address = prompt_until_valid("Adres: ", validate_address)
    index_number = prompt_until_valid("Numer indeksu: ", validate_index_number)

    while True:
        pesel = prompt_until_valid("PESEL (11 cyfr): ", validate_pesel_format)
        gender = prompt_until_valid("Płeć (M/K): ", validate_gender)
        try:
            validate_pesel(pesel, gender)
            break
        except ValidationError as e:
            print(f"[BŁĄD] {e}")
            print("Spróbuj ponownie: popraw PESEL i/lub płeć.\n")

    return Student(
        first_name=first_name,
        last_name=last_name,
        address=address,
        index_number=index_number,
        pesel=pesel,
        gender=gender,
    )



def read_updates() -> dict:
    print("Zostaw puste, jeśli bez zmian. (Możesz też zostawić puste po błędzie, żeby pominąć.)")
    updates = {}

    first_name = prompt_optional("Nowe imię: ", lambda v: validate_name(v, "Imię"))
    if first_name is not None:
        updates["first_name"] = first_name

    last_name = prompt_optional("Nowe nazwisko: ", lambda v: validate_name(v, "Nazwisko"))
    if last_name is not None:
        updates["last_name"] = last_name

    address = prompt_optional("Nowy adres: ", validate_address)
    if address is not None:
        updates["address"] = address

    pesel = prompt_optional("Nowy PESEL: ", validate_pesel_format)
    if pesel is not None:
        updates["pesel"] = pesel

    gender = prompt_optional("Nowa płeć (M/K): ", validate_gender)
    if gender is not None:
        updates["gender"] = gender

    return updates


def print_students(students: list[Student]) -> None:
    if not students:
        print("Brak studentów w bazie.")
        return
    
    print("\n--- Lista studentów ---")
    for s in students:
        print(f"- {s.first_name} {s.last_name} | indeks: {s.index_number} | PESEL: {s.pesel} | płeć: {s.gender} | adres: {s.address}")
        