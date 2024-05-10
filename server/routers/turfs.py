from fastapi import APIRouter
from .types import turf
import uuid
from fastapi import Request

router = APIRouter()

insert_query = """
INSERT INTO public.turf (uuid, user_uuid, name, address, phone, email, start_time, end_time, days_available, price_per_hr, currency, max_people, turf_length, turf_width, grass, advance_days, advance_end_in_mins)
VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17);
"""

delete_query = """
DELETE FROM public.turf where uuid = $1;
"""

update_query = """
UPDATE public.turf
SET name = $1, address = $2, phone = $3, email = $4, start_time = $5, end_time = $6, days_available = $7, price_per_hr = $8, currency = $9, max_people = $10, turf_length = $11, turf_width = $12, grass = $13, advance_days = $14, advance_end_in_mins = $15
WHERE uuid = $16 
"""

@router.post("/turfs/", tags=["turfs"])
async def write_turf(turf: turf.Turf, request: Request):
    turf_uuid = uuid.uuid4()
    result = await request.app.state.db.save_row(
        insert_query,
        turf_uuid,
        turf.user_uuid,
        turf.name,
        turf.address,
        turf.phone,
        turf.email,
        turf.start_time,
        turf.end_time,
        turf.days_available,
        turf.price_per_hr,
        turf.currency,
        turf.max_people,
        turf.turf_length,
        turf.turf_width,
        turf.grass,
        turf.advance_days,
        turf.advance_end_in_mins
    )
    return {"message":"create successful"}

@router.get("/turfs/{turf_uuid}/delete/", tags=["turfs"])
async def delete_turf(turf_uuid:str, request: Request):
    result = await request.app.state.db.delete_row(
        delete_query,
        turf_uuid
    )
    return {"message":"delete successful"}

@router.put("/turfs/{turf_uuid}/update/", tags=["turfs"])
async def update_turf(turf_uuid: int, turf: turf.Turf, request: Request):
    result = await request.app.state.db.update_row(
        update_query,
        turf.name,
        turf.address,
        turf.phone,
        turf.email,
        turf.start_time,
        turf.end_time,
        turf.days_available,
        turf.price_per_hr,
        turf.currency,
        turf.max_people,
        turf.turf_length,
        turf.turf_width,
        turf.grass,
        turf.advance_days,
        turf.advance_end_in_mins,
        turf_uuid 
    )
    return {"message":"update successful"}
    