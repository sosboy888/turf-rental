from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .routers import users
from dotenv import dotenv_values

config = dotenv_values('.env')
app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Turf Central!"}