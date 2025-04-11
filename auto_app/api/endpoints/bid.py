from typing import List
from auto_app.db.models import Bid
from auto_app.db.schema import BidSchema
from fastapi import APIRouter, Depends, HTTPException
from auto_app.db.database import SessionLocal
from sqlalchemy.orm import Session

bid_router = APIRouter(prefix='/bid', tags=['Bid'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@bid_router.post("/create", response_model=BidSchema)
async def bid_create(task: BidSchema, db: Session = Depends(get_db)):
    bid_db = Bid(**task.dict())
    db.add(bid_db)
    db.commit()
    db.refresh(bid_db)
    return bid_db


@bid_router.get('/', response_model=List[BidSchema])
async def bid_list(db: Session = Depends(get_db)):
    return db.query(Bid).all()


@bid_router.get('/{bid_id}', response_model=BidSchema)
async def bid_detail(bid_id: int, db: Session = Depends(get_db)):
    bid = db.query(Bid).filter(Bid.id == bid_id).first()

    if bid is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')
    return bid


@bid_router.put('/{bid_id}', response_model=BidSchema)
async def bid_update(bid_id: int, bid: BidSchema, db: Session = Depends(get_db)):
    bid_db = db.query(Bid).filter(Bid.id == bid_id).first()

    if bid_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')


    for bid_key, bid_values in bid.dict().items():
        setattr(bid_db, bid_key, bid_values)

    db.add(bid_db)
    db.commit()
    db.refresh(bid_db)
    return bid_db


@bid_router.delete('/{bid_id}')
async def bid_delete(bid_id: int, db: Session = Depends(get_db)):
    bid_db = db.query(Bid).filter(Bid.id == bid_id).first()

    if bid_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    db.delete(bid_db)
    db.commit()
    return {"message": "This is deleted"}
