from pydantic import BaseModel
from datetime import date
"""
uuid - Primary key
username - TEXT
password_hash - TEXT
dob - DATE
email - TEXT NULLABLE (either email or phone is required)
phone - TEXT NULLABLE
category - TEXT(USER, ADMIN, or TURF_ADMIN)
description - TEXT
profile_pic_url - TEXT
"""

class User(BaseModel):
    uuid: str
    username: str
    password_hash: str
    dob: date
    email: str
    phone: str
    category: str
    description: str
    profile_pic_url: str
