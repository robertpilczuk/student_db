import pytest

from models import Student
from repository import StudentRepository
from exceptions import DuplicateError, NotFoundError, ValidationError


def make_student(
        first="Jan",
        last="Kowalski",
        address="Lublin, ul. Projekotwa 2",
        index_number="S0001",
    pesel="99010501230",  
    gender="M",
):
    return Student(
        first_name=first,
        last_name=last,
        address=address,
        index_number=index_number,
        pesel=pesel,
        gender=gender,
    )


def test_add_student_ok():
    repo = StudentRepository([])
    repo.add(make_student())
    assert len(repo.all()) == 1


def test_add_duplicate_index_raises():
    repo = StudentRepository([])
    repo.add(make_student(index_number="S0001"))
    with pytest.raises(DuplicateError):
        repo.add(make_student(index_number="S0001", pesel="99010501247", gender="K"))


def test_add_duplicate_pesel_raises():
    repo = StudentRepository([])
    repo.add(make_student(pesel="99010501230", gender="M"))
    with pytest.raises(DuplicateError):
        repo.add(make_student(index_number="S0002", pesel="99010501230", gender="M"))


def test_find_by_pesel_ok():
    repo = StudentRepository([make_student()])
    s = repo.find_by_pesel("99010501230")
    assert s.last_name == "Kowalski"


def test_find_by_pesel_not_found():
    repo = StudentRepository([])
    with pytest.raises(NotFoundError):
        repo.find_by_pesel("99010501230")


def test_find_by_last_name_case_insensitive():
    repo = StudentRepository([
        make_student(last="Nowak", index_number="S0001", pesel="99010501230", gender="M"),
        make_student(last="nowak", index_number="S0002", pesel="99010501247", gender="K"),
    ])
    res = repo.find_by_last_name("NoWaK")
    assert len(res) == 2


def test_sort_by_last_name():
    repo = StudentRepository([
        make_student(first="A", last="Zebra", index_number="S0001", pesel="99010501230", gender="M"),
        make_student(first="B", last="Adam", index_number="S0002", pesel="99010501247", gender="K"),
    ])
    repo.sort_by_last_name()
    all_s = repo.all()
    assert all_s[0].last_name.lower() == "adam"
    assert all_s[1].last_name.lower() == "zebra"


def test_delete_by_index_ok():
    repo = StudentRepository([make_student(index_number="S0001")])
    repo.delete_by_index("S0001")
    assert repo.all() == []


def test_delete_by_index_not_found():
    repo = StudentRepository([])
    with pytest.raises(NotFoundError):
        repo.delete_by_index("S9999")


def test_update_student_ok_change_address():
    repo = StudentRepository([make_student(index_number="S0001")])
    repo.update("S0001", address="Nowy adres 123")
    assert repo.all()[0].address == "Nowy adres 123"


def test_update_unknown_field_raises():
    repo = StudentRepository([make_student(index_number="S0001")])
    with pytest.raises(ValidationError):
        repo.update("S0001", unknown_field="x") 


def test_update_change_pesel_and_gender_ok():
    repo = StudentRepository([make_student(index_number="S0001")])
    repo.update("S0001", pesel="99010501247", gender="K")
    assert repo.all()[0].pesel == "99010501247"
    assert repo.all()[0].gender == "K"


def test_update_gender_mismatch_raises():
    repo = StudentRepository([make_student(index_number="S0001")])
    with pytest.raises(ValidationError):
        repo.update("S0001", gender="K")