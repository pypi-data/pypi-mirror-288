from __future__ import annotations

from dataclasses import dataclass

ID: int = 0
USER_ID: int = 1
DATE_ID: int = 2
RESPONSE: int = 3
    
@dataclass
class Answer:
    
    
    id: int
    user_id: int
    date_id: int
    response: bool

    @classmethod
    def create_table(cls):
        return """ CREATE TABLE IF NOT EXISTS answers (
            id integer PRIMARY KEY AUTOINCREMENT,
            user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            date_id integer NOT NULL REFERENCES dates(id) ON DELETE CASCADE,
            response boolean NOT NULL,
            UNIQUE(user_id, date_id)
        ); """
     
    @classmethod   
    def toResource(cls, row) -> Answer:
        return Answer(
            id=row[ID],
            user_id=row[USER_ID],
            date_id=row[DATE_ID],
            response=bool(row[RESPONSE])
        )
