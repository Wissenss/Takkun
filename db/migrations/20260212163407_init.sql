-- migrate:up
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

-- migrate:down
DROP TABLE IF EXISTS training_sessions;
DROP TABLE IF EXISTS accounts;
