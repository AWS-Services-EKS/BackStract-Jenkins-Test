from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException
import models, schemas
import boto3

import jwt

import datetime

from pathlib import Path

async def get_categories(db: Session):

    categories_all = db.query(models.Categories).all()
    categories_all = [new_data.to_dict() for new_data in categories_all] if categories_all else categories_all

    res = {
        'categories_all': categories_all,
    }
    return res

async def get_categories_id(db: Session, id: int):

    categories_one = db.query(models.Categories).filter(models.Categories.id == id).first() 
    categories_one = categories_one.to_dict() if categories_one else categories_one

    res = {
        'categories_one': categories_one,
    }
    return res

async def post_categories(db: Session, raw_data: schemas.PostCategories):
    id:str = raw_data.id
    name:str = raw_data.name
    description:str = raw_data.description


    record_to_be_added = {'id': id, 'name': name, 'description': description}
    new_categories = models.Categories(**record_to_be_added)
    db.add(new_categories)
    db.commit()
    db.refresh(new_categories)
    categories_inserted_record = new_categories.to_dict()



    user: str = name


    

    try:
        strd = user_list[0]
    except Exception as e:
        raise HTTPException(500, str(e))


    res = {
        'categories_inserted_record': categories_inserted_record,
    }
    return res

async def put_categories_id(db: Session, raw_data: schemas.PutCategoriesId):
    id:str = raw_data.id
    name:str = raw_data.name
    description:str = raw_data.description


    categories_edited_record = db.query(models.Categories).filter(models.Categories.id == id).first()
    for key, value in {'id': id, 'name': name, 'description': description}.items():
          setattr(categories_edited_record, key, value)
    db.commit()
    db.refresh(categories_edited_record)
    categories_edited_record = categories_edited_record.to_dict() 

    res = {
        'categories_edited_record': categories_edited_record,
    }
    return res

async def delete_categories_id(db: Session, id: int):

    categories_deleted = None
    record_to_delete = db.query(models.Categories).filter(models.Categories.id == id).first()

    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        categories_deleted = record_to_delete.to_dict() 

    res = {
        'categories_deleted': categories_deleted,
    }
    return res

async def get_users(db: Session):

    users_all = db.query(models.Users).all()
    users_all = [new_data.to_dict() for new_data in users_all] if users_all else users_all

    res = {
        'users_all': users_all,
    }
    return res

async def get_users_id(db: Session, id: int):

    users_one = db.query(models.Users).filter(models.Users.id == id).first() 
    users_one = users_one.to_dict() if users_one else users_one

    res = {
        'users_one': users_one,
    }
    return res

async def post_users(db: Session, raw_data: schemas.PostUsers):
    id:str = raw_data.id
    firstname:str = raw_data.firstname
    lastname:str = raw_data.lastname


    record_to_be_added = {'id': id, 'firstname': firstname, 'lastname': lastname}
    new_users = models.Users(**record_to_be_added)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    users_inserted_record = new_users.to_dict()

    res = {
        'users_inserted_record': users_inserted_record,
    }
    return res

async def put_users_id(db: Session, raw_data: schemas.PutUsersId):
    id:str = raw_data.id
    firstname:str = raw_data.firstname
    lastname:str = raw_data.lastname


    users_edited_record = db.query(models.Users).filter(models.Users.id == id).first()
    for key, value in {'id': id, 'firstname': firstname, 'lastname': lastname}.items():
          setattr(users_edited_record, key, value)
    db.commit()
    db.refresh(users_edited_record)
    users_edited_record = users_edited_record.to_dict() 

    res = {
        'users_edited_record': users_edited_record,
    }
    return res

async def delete_users_id(db: Session, id: int):

    users_deleted = None
    record_to_delete = db.query(models.Users).filter(models.Users.id == id).first()

    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        users_deleted = record_to_delete.to_dict() 

    res = {
        'users_deleted': users_deleted,
    }
    return res

