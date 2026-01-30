from pathlib import Path
from exceptions import StudentDbError, StorageError
from repository import StudentRepository
from storage import load_students, save_students, DEFAULT_PATH
from ui import print_menu, read_student, print_students


def main(db_path: Path = DEFAULT_PATH) -> None:
    try:
        students = load_students(db_path)
    except StorageError as e:
        print(f"[BŁAD] Nie udało się wczytać bazy: {e}")
        students = []

    repo = StudentRepository(students)

    while True:
        print_menu()
        choice = input("Wybierz opcję: ").strip()

        try:
            if choice == "":
                student = read_student()
                repo.add(student)
                print("Dodano studenta.")

            elif choice == "2":
                print_students(repo.all())

            elif choice == "3":
                ln = input("Podaj nazwisko: ").strip()
                results = repo.find_by_last_name(ln)
                print_students(results)

            elif choice == "4":
                pesel = input("Podaj PESEL: ").strip()
                s = repo.find_by_pesel(pesel)
                print_students([s])

            elif choice == "5":
                repo.sort_by_pesel()
                print("Posortowano wg PESEL.")

            elif choice == "6":
                repo.sort_by_last_name()
                print("{Posortowano wg nazwiska.}")

            elif choice == "7":
                idx = input("Podaj numer indeksu do usunięcia: ").strip()
                repo.delete_by_index(idx)
                print("Usunięto studenta.")

            elif choice == "8":
                idx = input("Podaj numer indeksu studenta do aktualizacji: ").strip()
                print("Zostaw puste jeśli bez zmian.")
                first_name = input("Nowe imię: ").strip()
                last_name = input("Nowe nazwisko: ").strip()
                address = input("Nowy adres: ").strip()
                pesel = input("Nowy PESEL: ").strip()
                gender = input("Nowa płeć (M/K): ").strip().upper()

                updates = {}
                if first_name: updates["first_name"] = first_name
                if last_name: updates["last_name"] = last_name
                if address: updates["address"] = address
                if pesel: updates["pesel"] = pesel
                if gender: updates["gender"] = gender

                repo.update(idx, **updates)
                print("Zaktualizowano dane studenta.")

            elif choice == "9":
                save_students(repo.all(), db_path)
                print("Zapisano bazę danych do pliku.")

            elif choice == "0":
                save_students(repo.all(), db_path)
                print("Zapisano i zakończono.")
                break
            else:
                print("Nieznana opcja.")
        except StudentDbError as e:
            print(f"[BŁAD] {e}")
        except Exception as e:
            print(f"[BŁAD NIEOCZEKIWANY] {e}")

if __name__ == "__main__":
    main()