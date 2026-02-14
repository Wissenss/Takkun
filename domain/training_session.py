from datetime import datetime
from typing import Optional, List
import sqlite3

from utils import DBUtils

class TTrainingSession:
  def __init__(self):
    self.id : int = 0
    self.account_id : int = 0
    self.created_at : datetime = datetime.now()
    self.updated_at : datetime = datetime.now()

  @staticmethod
  def from_row(row: tuple) -> "TTrainingSession":
    session = TTrainingSession()
    
    session.id = row[0]
    session.account_id = row[1]
    session.created_at = DBUtils.parse_datetime_str(row[2])
    session.updated_at = DBUtils.parse_datetime_str(row[3])
    
    return session
  
  def to_dict(self) -> dict:
    return {
        "id": self.id,
        "account_id": self.account_id,
        "created_at": DBUtils.format_db_date(self.created_at),
        "updated_at": DBUtils.format_db_date(self.updated_at),
    }

class TrainingSessionRepo:
  def __init__(self):
    pass 

  @classmethod
  def Create(cls, conn: sqlite3.Connection, session: TTrainingSession) -> TTrainingSession:
    now = datetime.now().isoformat()

    cursor = conn.cursor()
    cursor.execute("""
      INSERT INTO training_sessions (account_id, created_at, updated_at)
      VALUES (?, datetime('now'), datetime('now'))
    """, [session.account_id])

    conn.commit()

    return TrainingSessionRepo.Read(conn, cursor.lastrowid)

  @classmethod
  def Read(cls, conn: sqlite3.Connection, session_id: int) -> Optional[TTrainingSession]:
    cursor = conn.cursor()
    cursor.execute("""
      SELECT id, account_id, created_at, updated_at
      FROM training_sessions
      WHERE id = ?
    """, (session_id,))

    row = cursor.fetchone()
    if not row:
      return None

    return TTrainingSession.from_row(row)

  @classmethod
  def ReadMultiple(cls, conn: sqlite3.Connection, account_id: Optional[int] = None) -> List[TTrainingSession]:
    cursor = conn.cursor()

    if account_id:
      cursor.execute("""
        SELECT id, account_id, created_at, updated_at
        FROM training_sessions
        WHERE account_id = ?
      """, (account_id,))
    else:
      cursor.execute("""
        SELECT id, account_id, created_at, updated_at
        FROM training_sessions
      """)

    rows = cursor.fetchall()
    return [TTrainingSession.from_row(row) for row in rows]

  @classmethod
  def Delete(cls, conn: sqlite3.Connection, session_id: int) -> None:
    cursor = conn.cursor()
    cursor.execute("""
      DELETE FROM training_sessions
      WHERE id = ?
    """, (session_id,))
    conn.commit()