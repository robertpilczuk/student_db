from models import Student
from validators import (
    validate_name,
    validate_address,
    validate_index_number,
    validate_pesel_format,
    validate_gender,
)


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


def read_student() -> Student:
    first_name = validate_name(input("Imię: "), "Imię")
    last_name = validate_name(input("Nazwisko: "), "Nazwisko")
    address = validate_address(input("Adres: "))
    index_number = validate_index_number(input("Numer indeksu: "))
    pesel = validate_pesel_format(input("PESEL (11 cyfr): "))
    gender = validate_gender(input("Płeć (M/K): "))

    return Student(
        first_name=first_name,
        last_name=last_name,
        address=address,
        index_number=index_number,
        pesel=pesel,
        gender=gender,
    )

def print_students(students: list[Student]) -> None:
    if not students:
        print("Brak studentów w bazie.")
        return
    
    print("\n--- Lista studentów ---")
    for s in students:
        print(f"- {s.first_name} {s.last_name} | indeks: {s.index_number} | PESEL: {s.pesel} | płeć: {s.gender} | adres: {s.address}")
        