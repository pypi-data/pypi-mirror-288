from __future__ import annotations

from dataclasses import dataclass
from typing import cast

ID: int = 0
NAME: int = 1
RANK: int = 2

@dataclass
class Instrument:
    
    id: int
    name: str
    rank: int

    @classmethod
    def create_table(cls):
        return """CREATE TABLE IF NOT EXISTS instruments (
            id integer PRIMARY KEY,
            name text NOT NULL UNIQUE,
            rank number NOT NULL UNIQUE
        );
        """
        
    @classmethod
    def toResource(cls, row) -> Instrument:
        return Instrument(
            id=row[ID],
            name=row[NAME],
            rank=row[RANK]
        )
    
    def __hash__(self) -> int:
        return self.id
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Instrument) and self.id == cast(Instrument, other).id