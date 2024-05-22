from fastapi import Depends, FastAPI

from dependencies import get_current_user
from routers import users, turfs
from db import database as db
from dotenv import dotenv_values
from logging.config import dictConfig
import logging
from logger_module.logger_module import LogConfig
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

dictConfig(LogConfig().dict())
logger = logging.getLogger("turfcentral")

"""LOGGER TEST"""
logger.info("Dummy Info")
logger.error("Dummy Error")
logger.debug("Dummy Debug")
logger.warning("Dummy Warning")

app = FastAPI()


app.include_router(users.router)
app.include_router(turfs.router)

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
    app.state.SECRET_KEY=config["jwt_secret_key"]
    logger.info("Server Startup")

@app.on_event("shutdown")
async def shutdown_event():
    if not app.state.db:
        await app.state.db.close()
    logger.info("Server Shutdown")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
get_user_query = """
SELECT (password_hash = crypt($2, password_hash)) 
    AS password_match 
FROM public."user"
WHERE email = $1 ;
"""

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, app.state.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    result = await app.state.db.fetch_row(
        get_user_query,
        form_data.username,
        form_data.password
    )
    print(result)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}