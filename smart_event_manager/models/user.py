from dataclasses import dataclass

@dataclass
class User:
    username: str

@dataclass
class Admin(User):
    pass
