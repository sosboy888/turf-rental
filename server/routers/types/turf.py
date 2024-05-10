from pydantic import BaseModel
from datetime import date, datetime, time

"""
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
)
"""

class Turf(BaseModel):
    user_uuid: str
    name: str
    address: str
    phone: str
    email: str
    start_time: time
    end_time: time
    days_available: str
    price_per_hr: int
    currency: str
    max_people: int
    turf_length: int
    turf_width: int
    grass: bool
    advance_days: int
    advance_end_in_mins: int
