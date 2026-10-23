-- Personalized Travel Itinerary Planner
-- Run this in the Supabase SQL editor (Milestone 2.2)

create extension if not exists "pgcrypto";

create table if not exists profiles (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  email text not null unique,
  password_hash text not null,
  created_at timestamptz not null default now()
);

create table if not exists preferences (
  user_id uuid primary key references profiles(id) on delete cascade,
  budget_min numeric,
  budget_max numeric,
  currency text default 'USD',
  vibe text default 'culture',
  climate text,
  companions text default 'solo',
  interests text[] default '{}',
  pace text default 'moderate',
  dietary text,
  mobility text,
  season text,
  travelers integer default 1,
  updated_at timestamptz not null default now()
);

create table if not exists destinations (
  id text primary key,
  name text not null,
  country text not null,
  region text,
  vibes text[] default '{}',
  climates text[] default '{}',
  budget_tier text,
  lat double precision,
  lng double precision,
  summary text
);

create table if not exists trips (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references profiles(id) on delete cascade,
  title text not null,
  destination_id text,
  destination text not null,
  start_date date not null,
  end_date date not null,
  budget numeric,
  vibe text,
  interests text[] default '{}',
  notes text,
  travelers integer default 1,
  dietary text,
  mobility text,
  pace text,
  travel_style text,
  companions text default 'solo',
  share_token text unique,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists itinerary_days (
  id uuid primary key default gen_random_uuid(),
  trip_id uuid not null references trips(id) on delete cascade,
  day_number integer not null,
  date date,
  theme text,
  summary text,
  unique (trip_id, day_number)
);

create table if not exists activities (
  id uuid primary key default gen_random_uuid(),
  day_id uuid not null references itinerary_days(id) on delete cascade,
  time_slot text not null,
  start_time text,
  end_time text,
  title text not null,
  description text,
  location text,
  category text,
  vibe text,
  lat double precision,
  lng double precision,
  estimated_cost numeric default 0,
  duration_minutes integer,
  travel_minutes integer default 0,
  sort_order integer not null default 0
);

create table if not exists recommendation_logs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references profiles(id) on delete cascade,
  prompt text,
  result jsonb,
  created_at timestamptz not null default now()
);

alter table profiles enable row level security;
alter table preferences enable row level security;
alter table trips enable row level security;
alter table itinerary_days enable row level security;
alter table activities enable row level security;
alter table recommendation_logs enable row level security;

alter table trips add column if not exists travelers integer default 1;
alter table trips add column if not exists dietary text;
alter table trips add column if not exists mobility text;
alter table trips add column if not exists pace text;
alter table trips add column if not exists travel_style text;
alter table trips add column if not exists companions text default 'solo';
alter table trips add column if not exists share_token text;

-- Backend uses the service role key, which bypasses RLS.
-- Anon policies are left closed so the browser cannot write directly.
