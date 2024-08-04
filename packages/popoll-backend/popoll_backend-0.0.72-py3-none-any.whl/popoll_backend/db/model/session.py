from __future__ import annotations

from dataclasses import dataclass

import datetime
import sqlite3

from popoll_backend.db import getOne, insert, update


ID: int = 0
SESSION_ID: int = 1
USER_ID: int = 2
@dataclass
class Session:
    
    id: int
    session_id: str
    user_id: int

    @classmethod
    def create_table(cls):
        return """CREATE TABLE IF NOT EXISTS sessions (
            id integer PRIMARY KEY,
            session_id text NOT NULL,
            user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            datetime text NOT NULL
        );"""

    @classmethod
    def toResource(cls, row) -> Session:
        return Session(
            id=row[ID],
            session_id=row[SESSION_ID],
            user_id=row[USER_ID]
        )
        
    @classmethod
    def create(cls, cursor: sqlite3.Cursor, session_id: str, user_id: int) -> Session:
        return insert(Session, cursor, 'INSERT INTO sessions(session_id, user_id, datetime) VALUES(?, ?, ?) RETURNING id, session_id, user_id, datetime', (session_id, user_id, datetime.datetime.now().isoformat(sep='T', timespec='auto')))
    
    @classmethod
    def get(cls, cursor: sqlite3.Cursor, session_id: str) -> Session:
        return getOne(Session, cursor, 'SELECT id, session_id, user_id FROM sessions WHERE session_id=?', (session_id,))
    
    @classmethod
    def update(cls, cursor: sqlite3.Cursor, id: int, session_id: str, user_id: int) -> Session:
        return update(Session, cursor, 'UPDATE sessions SET session_id=?, user_id=? WHERE id=? RETURNING id, session_id, user_id, datetime', (session_id, user_id, id))