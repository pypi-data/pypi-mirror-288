from __future__ import annotations

from dataclasses import dataclass

NAME = 0
COLOR = 1

@dataclass
class Option:
    
    name: str
    color: str
    
    @classmethod
    def create_table(cls):
        return """ CREATE TABLE IF NOT EXISTS options (
            name text,
            color text 
        ); """
        
    @classmethod
    def toResource(cls, row) -> Option:
        return Option(
            name=row[NAME],
            color=row[COLOR]
        )