from fastapi import Depends, FastAPI

from dependencies import get_query_token, get_token_header
from routers import users
from db import database as db
from dotenv import dotenv_values
from logging.config import dictConfig
import logging
from logger_module.logger_module import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("turfcentral")

"""LOGGER TEST"""
logger.info("Dummy Info")
logger.error("Dummy Error")
logger.debug("Dummy Debug")
logger.warning("Dummy Warning")

"""
app = FastAPI(dependencies=[Depends(get_query_token)])
"""
app = FastAPI()

app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Turf Central!"}


@app.on_event("startup")
async def startup_event():
    config = dotenv_values('.env')
    global logger
    database_instance = db.Database(
        user = config['user'],
        password = config['password'],
        host = config['host'],
        database = config['database'],
        logger=logger
    )
    await database_instance.connect()
    app.state.db = database_instance
    logger.info("Server Startup")

@app.on_event("shutdown")
async def shutdown_event():
    if not app.state.db:
        await app.state.db.close()
    logger.info("Server Shutdown")