from __future__ import annotations

from dataclasses import dataclass
import datetime
from typing import Optional

def isOlder(actualDate: datetime.date, compare: datetime.date=datetime.date.today()):
    return actualDate < compare

ID: int = 0
TITLE: int = 1
DATE: int = 2
TIME: int = 3
END_TIME: int = 4
IS_FROZEN: int = 5

@dataclass
class Date:
    
    id: int
    title: str
    date: datetime.date
    time: Optional[datetime.time]
    end_time: Optional[datetime.time]
    is_frozen: bool
    is_old: bool
    

    @classmethod
    def create_table(cls):
        return """ CREATE TABLE IF NOT EXISTS dates (
            id integer PRIMARY KEY AUTOINCREMENT,
            title text NOT NULL,
            date text NOT NULL,
            time text,
            end_time text,
            is_frozen boolean NOT NULL
        ); """
    
    @classmethod    
    def toResource(cls, row) -> Date:
        date = datetime.date.fromisoformat(row[DATE])
        return Date(
            id=row[ID],
            title=row[TITLE],
            date=date,
            time=datetime.time.fromisoformat(row[TIME]) if row[TIME] else None,
            end_time=datetime.time.fromisoformat(row[END_TIME]) if row[END_TIME] else None,
            is_frozen=bool(row[IS_FROZEN]),
            is_old=isOlder(date)
        )
