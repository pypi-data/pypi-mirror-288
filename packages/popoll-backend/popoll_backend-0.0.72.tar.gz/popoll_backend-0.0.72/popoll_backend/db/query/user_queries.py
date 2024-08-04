import sqlite3
from typing import List

from popoll_backend.db import getSome, insert, update
from popoll_backend.db.model import user
from popoll_backend.db.model.instrument import Instrument
from popoll_backend.db.model.user import User
from popoll_backend.db.model.user_instruments import UserInstruments
from popoll_backend.usecases.poll.user.user_with_instruments import UserWithInstruments


class UserQueries:

    def create(self, cursor: sqlite3.Cursor, name: str) -> User:
        return insert(User, cursor, 'INSERT INTO users(name) VALUES(?) RETURNING id, name', (name,))

    def getUserWithInstruments(self, cursor: sqlite3.Cursor, id: int) -> UserWithInstruments:
        
        INSTRUMENT_ID: int = 2
        INSTRUMENT_NAME: int = 3
        INSTRUMENT_RANK: int = 4
        USER_INSTRUMENTS_ID: int = 5
        USER_INSTRUMENTS_IS_MAIN: int = 6
        
        rows = cursor.execute("""
            SELECT u.id, u.name, i.id, i.name, i.rank, ui.id, ui.is_main 
            FROM users as u 
            INNER JOIN user_instruments as ui
                ON u.id = ui.user_id
            INNER JOIN instruments as i
                ON ui.instrument_id = i.id
                AND ui.user_id = u.id
            WHERE u.id = ?
            ORDER BY i.rank
            """, (id,)).fetchall()
        return UserWithInstruments(
            User.toResource((rows[0][user.ID], rows[0][user.NAME],)),
            [Instrument.toResource((row[INSTRUMENT_ID], row[INSTRUMENT_NAME], row[INSTRUMENT_RANK],)) for row in rows],
            [UserInstruments.toResource((row[USER_INSTRUMENTS_ID], row[user.ID], row[INSTRUMENT_ID], row[USER_INSTRUMENTS_IS_MAIN],)) for row in rows]
        )
        
    def get_all(self, cursor: sqlite3.Cursor) -> List[User]:
        return getSome(User, cursor, 'SELECT id, name FROM users ORDER BY name COLLATE NOCASE')
    
    def update(self, cursor: sqlite3.Cursor, id: int, name: str) -> User:
        return update(User, cursor, 'UPDATE users SET name=? WHERE id=? RETURNING id, name', (name, id))
        
    def delete(self, cursor: sqlite3.Cursor, id: int) -> None:
        cursor.execute('DELETE FROM users WHERE id=?', (id,))
        return