## User table
uuid - Primary key
username - TEXT
password_hash - TEXT
dob - DATE
email - TEXT NULLABLE (either email or phone is required)
phone - TEXT NULLABLE
category - TEXT(USER, ADMIN, or TURF_ADMIN)
description - TEXT
profile_pic_url - TEXT

### Query - 
CREATE TABLE IF NOT EXISTS public."user"
(
    uuid uuid NOT NULL,
    username text COLLATE pg_catalog."default" NOT NULL,
    password_hash text COLLATE pg_catalog."default" NOT NULL,
    dob date NOT NULL,
    email text COLLATE pg_catalog."default",
    phone text COLLATE pg_catalog."default",
    category text COLLATE pg_catalog."default",
    description text COLLATE pg_catalog."default",
    profile_pic_url text COLLATE pg_catalog."default",
    CONSTRAINT user_pkey PRIMARY KEY (uuid)
) PARTITION BY HASH (uuid);

ALTER TABLE IF EXISTS public."user"
    OWNER to sosboy888;

### Turf table
uuid - Primary key
user_uuid - TEXT
name - TEXT
address - TEXT
phone - TEXT
email - TEXT
start_time - DATETIME
end_time - DATETIME
days_available - TEXT(WEEKDAYS or ALL_DAYS)
price_per_hr - INTEGER
currency - CHAR(basically a symbol like $)
max_people - INTEGER
turf_length - INTEGER
turf_width - INTEGER
grass - BOOLEAN
advance_days - INTEGER (the number of days in advance that a booking can be made)
advance_end_in_mins - INTEGER (the number of minutes before a time slot where the time slot is unbookable)

### Query - 
CREATE TABLE IF NOT EXISTS public.turf
(
    uuid uuid NOT NULL,
    user_uuid text COLLATE pg_catalog."default" NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    address text COLLATE pg_catalog."default" NOT NULL,
    phone text COLLATE pg_catalog."default" NOT NULL,
    email text COLLATE pg_catalog."default" NOT NULL,
    start_time time without time zone NOT NULL,
    end_time time without time zone NOT NULL,
    days_available text COLLATE pg_catalog."default" NOT NULL,
    price_per_hr integer NOT NULL,
    currency character(1) COLLATE pg_catalog."default" NOT NULL,
    max_people integer NOT NULL,
    turf_length integer NOT NULL,
    turf_width integer NOT NULL,
    grass boolean NOT NULL,
    "advance days" integer NOT NULL,
    advance_end_in_mins integer NOT NULL,
    CONSTRAINT turf_pkey PRIMARY KEY (uuid)
) PARTITION BY HASH (uuid);

ALTER TABLE IF EXISTS public.turf
    OWNER to sosboy888;

### Bookings table
uuid - Primary Key
turf_uuid - TEXT
user_uuid - TEXT
start_time - DATETIME
end_time - DATETIME
amount - INTEGER
currency - CHAR
no_of_people - INTEGER
sport_uuid - TEXT

### Query -
CREATE TABLE IF NOT EXISTS public.bookings
(
    uuid uuid NOT NULL,
    turf_uuid text COLLATE pg_catalog."default" NOT NULL,
    user_uuid text COLLATE pg_catalog."default" NOT NULL,
    start_time time without time zone NOT NULL,
    start_date date NOT NULL,
    end_time time without time zone NOT NULL,
    end_date date NOT NULL,
    amount integer NOT NULL,
    currency character(1) COLLATE pg_catalog."default" NOT NULL,
    no_of_people integer NOT NULL,
    sport_uuid text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT bookings_pkey PRIMARY KEY (uuid)
) PARTITION BY HASH (uuid);

ALTER TABLE IF EXISTS public.bookings
    OWNER to sosboy888;

### Sports table(to dynamically provide data about what sports a turf provides eg: soccer, cricket)
uuid - Primary Key
turf_uuid - TEXT
name - TEXT

CREATE TABLE IF NOT EXISTS public.sports
(
    uuid uuid NOT NULL,
    turf_uuid text COLLATE pg_catalog."default" NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT sports_pkey PRIMARY KEY (uuid)
) PARTITION BY HASH (uuid);

ALTER TABLE IF EXISTS public.sports
    OWNER to sosboy888;

