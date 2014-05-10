-- drop table if exists entries;
-- create table entries (
--   id integer primary key autoincrement,
--   title text not null,
--   text text not null
-- );

drop table if exists lounges;
create table lounges (
  id integer primary key autoincrement,
  building text,
  floor integer,
  free integer,
  reserve_start text,
  reserve_end text
);

drop table if exists reservations;
create table reservations (
  i integer primary key,
  id integer,
  reserve_start text,
  reserve_end text
);

INSERT INTO reservations (id, reserve_start, reserve_end) VALUES 
      (1, "03/31/2014 11:00", "03/31/2014 12:00" ),(25, "03/31/2014 11:00", "03/31/2014 12:00" ), 
      (49, "03/31/2014 11:00", "03/31/2014 12:00" );

INSERT INTO lounges (building, floor, free) VALUES 
      ('Harrison', 1, 2), ('Harrison', 2, 2), ('Harrison', 3, 2), ('Harrison', 4, 2), ('Harrison', 5, 2),
      ('Harrison', 6, 2), ('Harrison', 7, 2), ('Harrison', 8, 2), ('Harrison', 9, 2), ('Harrison', 10, 2),
      ('Harrison', 11, 2), ('Harrison', 12, 2), ('Harrison', 13, 2), ('Harrison', 14, 2), ('Harrison', 15, 2),
      ('Harrison', 16, 2), ('Harrison', 17, 2), ('Harrison', 18, 2), ('Harrison', 19, 2), ('Harrison', 20, 2),
      ('Harrison', 21, 2), ('Harrison', 22, 2), ('Harrison', 23, 2), ('Harrison', 24, 2),
      ('Rodin', 1, 2), ('Rodin', 2, 2), ('Rodin', 3, 2), ('Rodin', 4, 2), ('Rodin', 5, 2),
      ('Rodin', 6, 2), ('Rodin', 7, 2), ('Rodin', 8, 2), ('Rodin', 9, 2), ('Rodin', 10, 2),
      ('Rodin', 11, 2), ('Rodin', 12, 2), ('Rodin', 13, 2), ('Rodin', 14, 2), ('Rodin', 15, 2),
      ('Rodin', 16, 2), ('Rodin', 17, 2), ('Rodin', 18, 2), ('Rodin', 19, 2), ('Rodin', 20, 2),
      ('Rodin', 21, 2), ('Rodin', 22, 2), ('Rodin', 23, 2), ('Rodin', 24, 2),
      ('Harnwell', 1, 2), ('Harnwell', 2, 2), ('Harnwell', 3, 2), ('Harnwell', 4, 2), ('Harnwell', 5, 2),
      ('Harnwell', 6, 2), ('Harnwell', 7, 2), ('Harnwell', 8, 2), ('Harnwell', 9, 2), ('Harnwell', 10, 2),
      ('Harnwell', 11, 2), ('Harnwell', 12, 2), ('Harnwell', 13, 2), ('Harnwell', 14, 2), ('Harnwell', 15, 2),
      ('Harnwell', 16, 2), ('Harnwell', 17, 2), ('Harnwell', 18, 2), ('Harnwell', 19, 2), ('Harnwell', 20, 2),
      ('Harnwell', 21, 2), ('Harnwell', 22, 2), ('Harnwell', 23, 2), ('Harnwell', 24, 2);

