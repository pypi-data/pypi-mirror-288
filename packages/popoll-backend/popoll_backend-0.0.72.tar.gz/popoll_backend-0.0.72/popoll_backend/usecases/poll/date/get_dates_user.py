import sqlite3

from popoll_backend.db.query.date_queries import DateQueries
from popoll_backend.usecases.poll.date.dates_user import DatesUser
from popoll_backend.usecases.poll import PollQuery

class GetDatesUser(PollQuery):
    
    id: int
    
    def __init__(self, poll: str, id: int):
        super().__init__(poll)
        self.id = id
    
    def process(self, cursor: sqlite3.Cursor) -> DatesUser:
        return DateQueries().get_dates_user(cursor, self.id)
