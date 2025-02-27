from pydantic import BaseModel

import datetime

import uuid

from typing import Any, Dict, List, Tuple

class Categories(BaseModel):
    id: int
    name: str
    description: str


class ReadCategories(BaseModel):
    id: int
    name: str
    description: str
    class Config:
        from_attributes = True


class Users(BaseModel):
    id: int
    firstname: str
    lastname: str


class ReadUsers(BaseModel):
    id: int
    firstname: str
    lastname: str
    class Config:
        from_attributes = True




class PostCategories(BaseModel):
    id: str
    name: str
    description: str

    class Config:
        from_attributes = True



class PutCategoriesId(BaseModel):
    id: str
    name: str
    description: str

    class Config:
        from_attributes = True



class PostUsers(BaseModel):
    id: str
    firstname: str
    lastname: str

    class Config:
        from_attributes = True



class PutUsersId(BaseModel):
    id: str
    firstname: str
    lastname: str

    class Config:
        from_attributes = True

