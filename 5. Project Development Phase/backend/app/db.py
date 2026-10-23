import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .config import DATABASE_PATH, SCHEMA_PATH


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect() -> sqlite3.Connection:
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = connect()
    conn.executescript(Path(SCHEMA_PATH).read_text(encoding="utf-8"))
    extra = [
        "ALTER TABLE trips ADD COLUMN travelers INTEGER DEFAULT 1",
        "ALTER TABLE trips ADD COLUMN dietary TEXT",
        "ALTER TABLE trips ADD COLUMN mobility TEXT",
        "ALTER TABLE trips ADD COLUMN pace TEXT",
        "ALTER TABLE trips ADD COLUMN travel_style TEXT",
        "ALTER TABLE preferences ADD COLUMN travelers INTEGER DEFAULT 1",
        "ALTER TABLE trips ADD COLUMN share_token TEXT",
        "ALTER TABLE trips ADD COLUMN companions TEXT DEFAULT 'solo'",
    ]
    for sql in extra:
        try:
            conn.execute(sql)
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()


def dumps(value) -> str:
    if isinstance(value, (list, dict)):
        return json.dumps(value)
    if not value:
        return "[]"
    return json.dumps([part.strip() for part in str(value).split(",") if part.strip()])


def loads(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except json.JSONDecodeError:
        return [part.strip() for part in str(value).split(",") if part.strip()]


def row_to_dict(row) -> dict | None:
    if row is None:
        return None
    data = dict(row)
    if "interests" in data:
        data["interests"] = loads(data.get("interests"))
    return data


def new_id() -> str:
    return str(uuid.uuid4())
