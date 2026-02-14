from datetime import datetime
from typing import Optional, List
from utils import DBUtils

import sqlite3

class TAccount:
  def __init__(self):
    self.id : int = 0
    self.nickname : str = ""
    self.api_key : str = ""
    self.is_enabled : bool = True
    self.created_at : datetime = datetime.now()
    self.updated_at : datetime = datetime.now()

  @staticmethod
  def from_row(row: tuple) -> "TAccount":
    account = TAccount()
    account.id = row[0]
    account.nickname = row[1]
    account.api_key = row[2]
    account.is_enabled = bool(row[3])
    account.created_at = DBUtils.parse_datetime_str(row[4])
    account.updated_at = DBUtils.parse_datetime_str(row[5])
    return account

class AccountRepo:
  def __init__(self):
    pass

  @classmethod
  def Create(cls, conn: sqlite3.Connection, account: TAccount) -> TAccount:
    now = datetime.now().isoformat()

    cursor = conn.cursor()
    cursor.execute("""
      INSERT INTO accounts (nickname, api_key, is_enabled, created_at, updated_at)
      VALUES (?, ?, ?, datetime('now'), datetime('now'))
    """, (account.nickname, account.api_key, int(account.is_enabled), now, now))

    conn.commit()

    return AccountRepo.Read(conn, cursor.lastrowid)

  @classmethod
  def Get(cls, conn: sqlite3.Connection, account_id: int) -> Optional[TAccount]:
    cursor = conn.cursor()
    cursor.execute("""
      SELECT *
      FROM accounts
      WHERE id = ?
    """, (account_id,))

    row = cursor.fetchone()
    if not row:
      return None

    return TAccount.from_row(row)

  @classmethod
  def get_by_api_key(cls, conn: sqlite3.Connection, api_key: str) -> Optional[TAccount]:
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM accounts WHERE api_key = ?;", [api_key])
    
    row = cursor.fetchone()

    if not row:
      return None

    return TAccount.from_row(row)

  @classmethod
  def get_many(cls, conn: sqlite3.Connection) -> List[TAccount]:
    cursor = conn.cursor()
    cursor.execute("""
      SELECT *
      FROM accounts
    """)

    rows = cursor.fetchall()
    return [TAccount.from_row(row) for row in rows]

  @classmethod
  def Delete(cls, conn: sqlite3.Connection, account_id: int) -> None:
    cursor = conn.cursor()
    cursor.execute("""
      DELETE FROM accounts
      WHERE id = ?
    """, (account_id,))
    conn.commit()