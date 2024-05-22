from fastapi import APIRouter
from .types import user
from dependencies import get_current_user
import uuid
from fastapi import Request, Depends

router = APIRouter()

insert_query = """
INSERT INTO public."user" (uuid, username, password_hash, dob, email, phone, category, description, profile_pic_url)
VALUES ($1, $2, crypt($3, gen_salt('md5')), $4, $5, $6, $7, $8, $9);
 """

fetchone_query = """
SELECT * FROM public."user" WHERE uuid=$1;
"""

@router.get("/users/{user_uuid}/", tags=["users"])
async def read_user(user_uuid: str, request: Request, current_user: dict = Depends(get_current_user)):
    result = await request.app.state.db.fetch_row(
        fetchone_query,
        user_uuid
    )
    return result


@router.post("/users/", tags=["users"])
async def write_user(user: user.User, request: Request):
    #TODO create user using generated hash_key
    user_uuid = uuid.uuid4()
    result = await request.app.state.db.save_row(
                                    insert_query, 
                                    user_uuid,
                                    user.username,
                                    user.password_hash,
                                    user.dob,
                                    user.email,
                                    user.phone,
                                    user.category,
                                    user.description,
                                    user.profile_pic_url
                                    )
    return {"message":"create_successful"}