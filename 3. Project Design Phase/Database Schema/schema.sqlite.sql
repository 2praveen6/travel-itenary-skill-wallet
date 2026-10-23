CREATE TABLE IF NOT EXISTS profiles (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS preferences (
  user_id TEXT PRIMARY KEY,
  budget_min REAL,
  budget_max REAL,
  currency TEXT DEFAULT 'USD',
  vibe TEXT DEFAULT 'culture',
  climate TEXT,
  companions TEXT DEFAULT 'solo',
  interests TEXT DEFAULT '[]',
  pace TEXT DEFAULT 'moderate',
  dietary TEXT,
  mobility TEXT,
  season TEXT,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES profiles(id)
);

CREATE TABLE IF NOT EXISTS trips (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  title TEXT NOT NULL,
  destination_id TEXT,
  destination TEXT NOT NULL,
  start_date TEXT NOT NULL,
  end_date TEXT NOT NULL,
  budget REAL,
  vibe TEXT,
  interests TEXT DEFAULT '[]',
  notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES profiles(id)
);

CREATE TABLE IF NOT EXISTS itinerary_days (
  id TEXT PRIMARY KEY,
  trip_id TEXT NOT NULL,
  day_number INTEGER NOT NULL,
  date TEXT,
  theme TEXT,
  summary TEXT,
  FOREIGN KEY (trip_id) REFERENCES trips(id)
);

CREATE TABLE IF NOT EXISTS activities (
  id TEXT PRIMARY KEY,
  day_id TEXT NOT NULL,
  time_slot TEXT NOT NULL,
  start_time TEXT,
  end_time TEXT,
  title TEXT NOT NULL,
  description TEXT,
  location TEXT,
  category TEXT,
  vibe TEXT,
  lat REAL,
  lng REAL,
  estimated_cost REAL DEFAULT 0,
  duration_minutes INTEGER,
  travel_minutes INTEGER DEFAULT 0,
  sort_order INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY (day_id) REFERENCES itinerary_days(id)
);

CREATE TABLE IF NOT EXISTS recommendation_logs (
  id TEXT PRIMARY KEY,
  user_id TEXT,
  prompt TEXT,
  result TEXT,
  created_at TEXT NOT NULL
);
