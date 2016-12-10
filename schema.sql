drop table if exists synthia_config;
create table synthia_config (
  morning_time_min time,
  morning_time_max time,
  morning_reminder_message text,
  evening_time_min time,
  evening_time_max time,
  evening_song text,
  current_city text
);

-- Between what times do you normally leave in the morning? leaving time range
-- What would you like Synthia to remind you of in the morning? custom leaving reminder message
-- Between what times do you arrive home in the evening? coming home time range
-- What song would you like to hear when you come home? coming  home song
-- What is your current city?
