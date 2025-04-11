from typing import List
from auto_app.db.models import Car
from auto_app.db.schema import CarCreateSchema, CarOutSchema, CarUpdateSchema
from fastapi import APIRouter, Depends, HTTPException
from auto_app.db.database import SessionLocal
from sqlalchemy.orm import Session

car_router = APIRouter(prefix='/car', tags=['Car'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@car_router.get('/search', response_model=List[CarOutSchema])
async def search_car(brand: str, db: Session = Depends(get_db)):
    car_db = db.query(Car).filter(Car.brand.like(f'%{brand}%')).all()
    if not car_db :
        raise HTTPException(status_code=404, detail='Car Not Found')
    return car_db



@car_router.post("/create", response_model=CarCreateSchema)
async def car_create(car: CarCreateSchema, db: Session = Depends(get_db)):
    car_db = Car(**car.dict())
    db.add(car_db)
    db.commit()
    db.refresh(car_db)
    return car_db


@car_router.get('/', response_model=List[CarOutSchema])
async def car_list(db: Session = Depends(get_db)):
    return db.query(Car).all()


@car_router.get('/{car_id}', response_model=CarOutSchema)
async def car_detail(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()

    if car is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')
    return car


@car_router.put('/{car_id}', response_model=CarUpdateSchema)
async def car_update(car_id: int, car: CarUpdateSchema, db: Session = Depends(get_db)):
    car_db = db.query(Car).filter(Car.id == car_id).first()

    if car_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')


    for car_key, car_values in car.dict().items():
        setattr(car_db, car_key, car_values)

    db.add(car_db)
    db.commit()
    db.refresh(car_db)
    return car_db


@car_router.delete('/{car_id}')
async def car_delete(car_id: int, db: Session = Depends(get_db)):
    car_db = db.query(Car).filter(Car.id == car_id).first()

    if car_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    db.delete(car_db)
    db.commit()
    return {"message": "This is deleted"}
