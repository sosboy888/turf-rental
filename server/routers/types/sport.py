from pydantic import BaseModel


class Sport(BaseModel):
    turf_uuid: str
    name: str