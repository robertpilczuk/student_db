from models import Student


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
    first_name = input("Imię: ").strip()
    last_name = input("Nazwisko: ").strip()
    address = input("Adres: ").strip()
    index_number = input("Numer indeksu: ").strip()
    pesel = input("PESEL (11 cyfr): ").strip()
    gender = input("Płeć (M/K)").strip().upper()

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
        