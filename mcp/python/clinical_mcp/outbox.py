from __future__ import annotations
import json
import os
import sqlite3
import time
from dataclasses import dataclass
from typing import Any, Mapping, Optional

from .pii import sanitize_mapping

_SCHEMA = """
CREATE TABLE IF NOT EXISTS outbox (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts_unix REAL NOT NULL,
  run_id TEXT NOT NULL,
  topic TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',  -- pending|sent|dead
  last_error TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_outbox_pending ON outbox(status, id);
"""

@dataclass(frozen=True)
class OutboxMessage:
    id: int
    ts_unix: float
    run_id: str
    topic: str
    payload: dict[str, Any]

class Outbox:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=30, isolation_level=None)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(_SCHEMA)

    def enqueue(self, *, run_id: str, topic: str, payload: Mapping[str, Any]) -> int:
        safe = sanitize_mapping(payload)
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO outbox(ts_unix, run_id, topic, payload_json, status) VALUES(?,?,?,?, 'pending')",
                (time.time(), run_id, topic, json.dumps(safe, ensure_ascii=False)),
            )
            return int(cur.lastrowid)

    def fetch_next_pending(self) -> Optional[OutboxMessage]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, ts_unix, run_id, topic, payload_json FROM outbox WHERE status='pending' ORDER BY id ASC LIMIT 1"
            ).fetchone()
            if not row:
                return None
            msg_id, ts_unix, run_id, topic, payload_json = row
            return OutboxMessage(
                id=int(msg_id),
                ts_unix=float(ts_unix),
                run_id=str(run_id),
                topic=str(topic),
                payload=json.loads(payload_json),
            )

    def mark_sent(self, msg_id: int) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE outbox SET status='sent', last_error='' WHERE id=?", (msg_id,))

    def mark_dead(self, msg_id: int, err: str) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE outbox SET status='dead', last_error=? WHERE id=?", (err[:500], msg_id))
