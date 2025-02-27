from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List
import service, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/categories/')
async def get_categories(db: Session = Depends(get_db)):
    try:
        return await service.get_categories(db)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/categories/id')
async def get_categories_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.get_categories_id(db, id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/categories/')
async def post_categories(raw_data: schemas.PostCategories, db: Session = Depends(get_db)):
    try:
        return await service.post_categories(db, raw_data)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/categories/id/')
async def put_categories_id(raw_data: schemas.PutCategoriesId, db: Session = Depends(get_db)):
    try:
        return await service.put_categories_id(db, raw_data)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/categories/id')
async def delete_categories_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.delete_categories_id(db, id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/users/')
async def get_users(db: Session = Depends(get_db)):
    try:
        return await service.get_users(db)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/users/id')
async def get_users_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.get_users_id(db, id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/users/')
async def post_users(raw_data: schemas.PostUsers, db: Session = Depends(get_db)):
    try:
        return await service.post_users(db, raw_data)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/users/id/')
async def put_users_id(raw_data: schemas.PutUsersId, db: Session = Depends(get_db)):
    try:
        return await service.put_users_id(db, raw_data)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/users/id')
async def delete_users_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.delete_users_id(db, id)
    except Exception as e:
        raise HTTPException(500, str(e))

