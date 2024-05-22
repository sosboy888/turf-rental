from fastapi import APIRouter
from .types import sport
import uuid
from fastapi import Request

router = APIRouter()

insert_query = "INSERT INTO public.sports(uuid, turf_uuid, name) VALUES($1, $2, $3);"

update_query = """
UPDATE public.sports
SET name = $1
WHERE uuid = $2 and turf_uuid = $3;
"""

delete_query = """
DELETE FROM public.sports where uuid = $1 and turf_uuid = $2;
"""

fetch_query = """
SELECT * from public.sports where turf_uuid = $1;
"""


@router.post("/sports/", tags=["sports"])
async def write(sport: sport.Sport, request: Request):
    sport_uuid = uuid.uuid4()
    result = await request.app.state.db.save_row(
        insert_query,
        sport_uuid,
        sport.turf_uuid,
        sport.name
    )
    
    return {"message":"create successful"}

@router.put("/sports/{sport_uuid}/update/", tags=["sports"])
async def update_sport(sport_uuid:str, sport: sport.Sport, request: Request):
    result = await request.app.state.db.update_row(
        update_query,
        sport.name,
        sport_uuid,
        sport.turf_uuid
    )
    return {"message":"update successful"}

@router.post("/sports/{sport_uuid}/delete/", tags=["sports"])
async def delete_turf(sport_uuid:str, sport: sport.Sport, request: Request):
    result = await request.app.state.db.delete_row(
        delete_query,
        sport_uuid,
        sport.turf_uuid
    )
    return {"message":"delete successful"}

@router.get("/sports/{turf_uuid}/", tags=["sports"])
async def get_sport_by_turf(turf_uuid: str, request: Request):
    result = await request.app.state.db.fetch_rows(
        fetch_query,
        turf_uuid
    )
    return {"results": result}