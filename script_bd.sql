CREATE TABLE if not exists station (
id int primary key,
name text,
latitude real,
longitude real
);

CREATE TABLE if not exists measure (
dat text ,
station int,
wind_healing real,
wind_speed_avg real,
wind_speed_max real,
wind_speed_min real,
foreign key(station) references station(id)
primary key (dat, station)
);
