from fastapi import APIRouter
from types import User
from ..db.database import Database
router = APIRouter()


insert_query = "INSERT INTO USER(uuid, username, password_hash, dob, email, phone, category, description, profile_pic_url) VALUES($1, $2, crypt($3, gen_salt('md5')), $4, $5, $6, $7, $8, $9)"

@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}

@router.post("/users/", tags=["users"])
async def write_user(user: User):
    #TODO create user using generated hash_key
    result = await Database.save_row(
                                    insert_query, 
                                    uuid=user.uuid,
                                    username=user.username,
                                    password_hash=user.password_hash,
                                    dob=user.dob,
                                    email=user.email,
                                    phone=user.phone,
                                    category=user.category,
                                    description=user.description,
                                    profile_pic_url=user.profile_pic_url
                                    )
    return {"message":"create_successful"}