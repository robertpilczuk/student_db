from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class Student:
    first_name: str
    last_name: str
    address: str
    index_number: str
    pesel: str
    gender: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Student":
        return Student(
            first_name=data["first_name"],
            last_name=data["last_name"],
            address=data["address"],
            index_number=data["index_number"],
            pesel=data["pesel"],
            gender=data["gender"],
        )