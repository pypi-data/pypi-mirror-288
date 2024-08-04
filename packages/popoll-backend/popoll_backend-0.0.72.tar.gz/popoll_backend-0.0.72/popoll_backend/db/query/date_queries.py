from __future__ import annotations

from dataclasses import dataclass
import datetime
import sqlite3
from typing import List, Optional

from popoll_backend.db import getOne, getSome, insert, update
from popoll_backend.db.model import date
from popoll_backend.db.model.answer import Answer
from popoll_backend.db.model.date import Date
from popoll_backend.db.model.instrument import Instrument
from popoll_backend.db.model.user import User
from popoll_backend.db.model.user_instruments import UserInstruments
from popoll_backend.usecases.poll.date.date_details import DateDetails
from popoll_backend.usecases.poll.date.dates_user import DatesUser

def isOlder(actualDate: datetime.date, compare: datetime.date=datetime.date.today()):
    return actualDate < compare

class DateQueries:
    
    def create(self, cursor: sqlite3.Cursor, title: str, date: datetime.date, time: Optional[datetime.time], end_time: Optional[datetime.time], is_frozen: bool) -> Date:
        return insert(Date, cursor, 'INSERT INTO dates(title, date, time, end_time, is_frozen) VALUES (?, ?, ?, ?, ?) RETURNING id, title, date, time, end_time, is_frozen', (title, date, time, end_time, is_frozen))
    
    def get(self, cursor: sqlite3.Cursor, id: int) -> Date:
        return getOne(Date, cursor, 'SELECT id, title, date, time, end_time, is_frozen FROM dates WHERE id=? LIMIT 1', (id,))
    
    def get_all(self, cursor: sqlite3.Cursor) -> List[Date]:
        return getSome(Date, cursor, 'SELECT id, title, date, time, end_time, is_frozen FROM dates ORDER BY date, time')
    
    def get_date_details(self, cursor: sqlite3.Cursor, id: int) -> DateDetails:
        USER_ID = 6
        USER_NAME = 7
        ANSWER_ID = 8
        ANSWER_RESPONSE = 9
        INSTRUMENT_ID = 10
        INSTRUMENT_NAME = 11
        INSTRUMENT_RANK = 12
        USER_INSTRUMENTS_ID = 13
        USER_INSTRUMENTS_IS_MAIN = 14
        
        rows = cursor.execute("""
            SELECT d.id, d.title, d.date, d.time, d.end_time, d.is_frozen, u.id, u.name, a.id, a.response, i.id, i.name, i.rank, ui.id, ui.is_main
            FROM dates as d
            INNER JOIN answers as a
                ON a.date_id = ?
            INNER JOIN users as u
                ON a.user_id = u.id
            INNER JOIN user_instruments as ui
                ON a.user_id = ui.user_id
            INNER JOIN instruments as i
                ON i.id = ui.instrument_id
            WHERE d.id = ?
            """, (id, id)).fetchall()
        return DateDetails(
            date = Date.toResource((rows[0][date.ID], rows[0][date.TITLE], rows[0][date.DATE], rows[0][date.TIME], rows[0][date.END_TIME], rows[0][date.IS_FROZEN]),),
            answers = [Answer.toResource((row[ANSWER_ID], row[USER_ID], row[date.ID], row[ANSWER_RESPONSE]),) for row in rows],
            users = list(set([User.toResource((row[USER_ID], row[USER_NAME])) for row in rows])),
            instruments = list(set([Instrument.toResource((row[INSTRUMENT_ID], row[INSTRUMENT_NAME], row[INSTRUMENT_RANK]),) for row in rows])),
            user_instruments = [UserInstruments.toResource((row[USER_INSTRUMENTS_ID], row[USER_ID], row[INSTRUMENT_ID], row[USER_INSTRUMENTS_IS_MAIN]),) for row in rows]
        )
        
    def get_dates_user(self, cursor: sqlite3.Cursor, user_id: int) -> DatesUser:
        USER_ID: int = 6
        USER_NAME: int = 7
        ANSWER_ID = 8
        ANSWER_RESPONSE = 9
        
        rows = cursor.execute("""
            SELECT d.id, d.title, d.date, d.time, d.end_time, d.is_frozen, u.id, u.name, a.id, a.response
            FROM dates as d
            LEFT JOIN answers as a
                ON a.user_id = ?
                AND a.date_id = d.id
            INNER JOIN users as u
                ON u.id = ?
            ORDER BY date, time
            """, (user_id, user_id)).fetchall()
        
        return DatesUser(
            user = User.toResource((rows[0][USER_ID], rows[0][USER_NAME]),),
            answers = [Answer.toResource((row[ANSWER_ID], row[USER_ID], row[date.ID], row[ANSWER_RESPONSE]),) for row in rows],
            dates = [Date.toResource((row[date.ID], row[date.TITLE], row[date.DATE], row[date.TIME], row[date.END_TIME], row[date.IS_FROZEN]),) for row in rows]
        )
        
    def update(self, cursor: sqlite3.Cursor, id: int, title: str, date: datetime.date, time: Optional[datetime.time], end_time: Optional[datetime.time], is_frozen: bool) -> Date:
        return update(Date, cursor, 'UPDATE dates SET title=?, date=?, time=?, end_time=?, is_frozen=? WHERE id=? RETURNING id, title, date, time, end_time, is_frozen', (title, date, time, end_time, is_frozen, id,))
        
    def delete(self, cursor: sqlite3.Cursor, id: int) -> None:
        cursor.execute('DELETE FROM dates WHERE id=?', (id,))
        return
    
    def delete_old_dates(self, cursor: sqlite3.Cursor, dateBefore: datetime.date) -> None:
        cursor.execute('DELETE FROM dates WHERE date < ?', (dateBefore,))