-- Run once in the Supabase SQL editor if trip create fails with PGRST204
-- (missing dietary / mobility / pace / travel_style / companions / travelers).

alter table trips add column if not exists travelers integer default 1;
alter table trips add column if not exists dietary text;
alter table trips add column if not exists mobility text;
alter table trips add column if not exists pace text;
alter table trips add column if not exists travel_style text;
alter table trips add column if not exists companions text default 'solo';
alter table trips add column if not exists share_token text;
alter table trips add column if not exists notes text;
alter table trips add column if not exists vibe text;
alter table trips add column if not exists interests text[] default '{}';
alter table trips add column if not exists budget numeric;
alter table trips add column if not exists destination_id text;

alter table preferences add column if not exists travelers integer default 1;
alter table preferences add column if not exists dietary text;
alter table preferences add column if not exists mobility text;
alter table preferences add column if not exists companions text default 'solo';
alter table preferences add column if not exists pace text default 'moderate';
alter table preferences add column if not exists interests text[] default '{}';

alter table activities add column if not exists duration_minutes integer;
alter table activities add column if not exists travel_minutes integer default 0;
alter table activities add column if not exists estimated_cost numeric default 0;
alter table activities add column if not exists category text;
alter table activities add column if not exists vibe text;
alter table activities add column if not exists start_time text;
alter table activities add column if not exists end_time text;
alter table activities add column if not exists location text;
alter table activities add column if not exists description text;
alter table activities add column if not exists lat double precision;
alter table activities add column if not exists lng double precision;
