from __future__ import annotations

from dataclasses import dataclass
from typing import cast

ID: int = 0
NAME: int = 1


@dataclass
class User:
    
    id: int
    name: str
    
    @classmethod
    def create_table(cls):
        return """ CREATE TABLE IF NOT EXISTS users (
            id integer PRIMARY KEY AUTOINCREMENT,
            name text NOT NULL UNIQUE COLLATE NOCASE
        ); """
        
    @classmethod
    def toResource(cls, row) -> User:
        return User(
            id=row[ID],
            name=row[NAME]
        )
        
    def __hash__(self) -> int:
        return self.id
    
    def __eq__(self, other) -> bool:
        return isinstance(other, User) and self.id == cast(User, other).id