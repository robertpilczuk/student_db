import json
from pathlib import Path
from typing import List
from models import Student
from exceptions import StorageError


DEFAULT_PATH = Path("data/student.json")


def load_students(path: Path=DEFAULT_PATH) -> List[Student]:
    try:
        if not path.exists():
            return []
        raw = path.read_text(encoding="utf-8").strip()
        if not raw:
            return []
        data = json.loads(raw)
        if not isinstance(data, list):
            raise StorageError("Plik JSON ma niepoprawny format (oczekiwano listy).")
        return [Student.from_dict(item) for item in data]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as e:
        raise StorageError(f"Błąd wczytywania pliku: {e}")
    

def save_students(students: List[Student], path: Path = DEFAULT_PATH) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = [s.to_dict() for s in students]
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as e:
        raise StorageError(f"Błąd zapisu pliku: {e}")
    
    