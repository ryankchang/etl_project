DROP SCHEMA IF EXISTS baseball_db;
CREATE SCHEMA baseball_db;
USE baseball_db;

DROP TABLE pitches;

CREATE TABLE pitches (
  ab_id INTEGER,
  ax REAL,
  ay REAL,
  az REAL,
  b_count INTEGER,
  b_score INTEGER,
  break_angle REAL,
  break_length REAL,
  break_y REAL,
  code TEXT,
  end_speed REAL,
  nasty REAL,
  on_1b INTEGER,
  on_2b INTEGER,
  on_3b INTEGER,
  outs INTEGER,
  pfx_x REAL,
  pfx_z REAL,
  pitch_num INTEGER,
  pitch_type TEXT,
  px REAL,
  pz REAL,
  s_count INTEGER,
  spin_dir REAL,
  spin_rate REAL,
  start_speed REAL,
  sz_bot REAL,
  sz_top REAL,
  type TEXT,
  type_confidence REAL,
  vx0 REAL,
  vy0 REAL,
  vz0 REAL,
  x REAL,
  x0 REAL,
  y REAL,
  y0 REAL,
  z0 REAL,
  zone REAL
);

CREATE TABLE atbats (
  ab_id INTEGER,
  batter_id INTEGER,
  event TEXT,
  g_id INTEGER,
  inning INTEGER,
  o INTEGER,
  p_score INTEGER,
  p_throws TEXT,
  pitcher_id INTEGER,
  stand TEXT,
  top INTEGER,
  primary key (ab_id)
);


CREATE TABLE games (
  g_id INTEGER,
  attendance TEXT,
  away_final_score INTEGER,
  away_team TEXT,
  date TEXT,
  elapsed_time TEXT,
  home_final_score INTEGER,
  home_team TEXT,
  start_time TEXT,
  umpire_1B TEXT,
  umpire_2B TEXT,
  umpire_3B TEXT,
  umpire_HP TEXT,
  venue_name TEXT,
  weather TEXT,
  wind TEXT,
  delay TEXT,
  primary key (g_id)
);

CREATE TABLE player_names (
  id INTEGER,
  first_name TEXT,
  last_name TEXT,
  name_url TEXT,
  name_url_edit TEXT,
  search_url TEXT,
  weight TEXT,
  primary key (id)
);

select * from atbats;
select * from games;
select * from player_names;
select * from pitches;

drop table player_names;
drop table atbats;
drop table games;
drop table pitches;*/

