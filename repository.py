from typing import List, Optional
from models import Student
from exceptions import DuplicateError, NotFoundError, ValidationError
from pesel import validate_pesel


class StudentRepository:
    def __init__(self, students: Optional[List[Student]] = None):
        self._students: List[Student] = students or []

    def all(self) -> List[Student]:
        return list(self._students)
    
    def add(self, student: Student) -> None:
        if any(s.index_number == student.index_number for s in self._students):
            raise DuplicateError("Student o podanym numerze indeksu ju istnieje.")
        if any(s.pesel == student.pesel for s in self._students):
            raise DuplicateError("Student o podanym numerze PESEL juz istnieje.")
        
        validate_pesel(student.pesel, student.gender)

        self._students.append(student)
    
    def delete_by_index(self, index_number: str) -> None:
        for i, s in enumerate(self._students):
            if s.index_number == index_number:
                del self._students[i]
                return
        raise NotFoundError("Nie znaleziono studenta o podanym numerze indeksu.")
    
    def find_by_pesel(self, pesel: str) -> Student:
        for s in self._students:
            if s.pesel == pesel:
                return s
        raise NotFoundError("Nie znaleziono studenta o podanym numerze PESEL.")
    
    def find_by_last_name(self, last_name: str) -> List[Student]:
        ln = last_name.strip().lower()
        return [s for s in self._students if s.last_name.strip().lower() == ln]
    
    def sort_by_pesel(self) -> None:
        self._students.sort(key=lambda s: s.pesel)

    def sort_by_last_name(self) -> None:
        self._students.sort(key=lambda s: (s.last_name.lower(), s.first_name.lower(), s.index_number))

    def update(self, index_number: str, **fields) -> None:
        student = None
        for s in self._students:
            if s.index_number == index_number:
                student = s
                break
        if student is None:
            raise NotFoundError("Nie znaleziono studenta o podanym numerze indeksu.")

        allowed = {"first_name", "last_name", "address", "pesel", "gender"}
        unknown = set(fields.keys()) - allowed
        if unknown:
            raise ValidationError(f"Nieznane pola do aktualizacji: {', '.join(sorted(unknown))}")

        new_pesel = fields.get("pesel", student.pesel)
        new_gender = fields.get("gender", student.gender)

        if new_pesel != student.pesel:
            if any(s.pesel == new_pesel for s in self._students):
                raise DuplicateError("Inny student ma już taki PESEL.")

        validate_pesel(new_pesel, new_gender)

        student.first_name = fields.get("first_name", student.first_name)
        student.last_name = fields.get("last_name", student.last_name)
        student.address = fields.get("address", student.address)
        student.pesel = new_pesel
        student.gender = new_gender