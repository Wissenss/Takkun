CREATE TABLE IF NOT EXISTS "migrations" (version varchar(128) primary key);
CREATE TABLE accounts(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nickname TEXT,
  api_key TEXT,
  is_enabled INTEGER,
  created_at TEXT,
  updated_at TEXT
);
CREATE TABLE training_sessions(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER NOT NULL,
  created_at TEXT,
  updated_at TEXT,
  FOREIGN KEY (account_id) REFERENCES accounts(id)
);
-- Dbmate schema migrations
INSERT INTO "migrations" (version) VALUES
  ('20260212163407');
