
from auto_app.db.database import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer, String, Enum, DateTime, ForeignKey,Text, DECIMAL
from typing import Optional,List
from enum import Enum as PyEnum, unique
from datetime import datetime
from passlib.hash import bcrypt


class RoleChoices(str, PyEnum):
    seller = 'seller'
    buyer = 'buyer'


class FueltypeChoices(str, PyEnum):
    benzin = 'benzin'
    dizel = 'dizel'
    hybrid = 'hybrid'
    electro = 'electro'
    gaz = 'gaz'

class TransmissionChoices(str, PyEnum):
    auto = 'auto'
    manual = 'manual'

class AuctionStatus(str, PyEnum):
    active = 'active 😊'
    completed = 'completed'
    canceled = 'canceled'


class UserProfile(Base):

    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    username: Mapped[str] = mapped_column(String,unique=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    phone_number: Mapped[Optional[str]]= mapped_column(String,nullable=True)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices))
    email: Mapped[str] = mapped_column(String, nullable=False,unique=True)
    seller: Mapped[List['Car']] = relationship('Car', back_populates='seller',
                                               cascade='all, delete-orphan')
    feed_seller: Mapped[List['Feedback']] = relationship('Feedback', back_populates='seller',
                                                         cascade='all, delete-orphan', foreign_keys='[Feedback.seller_id]')
    feed_buyer: Mapped[List['Feedback']] = relationship('Feedback', back_populates='buyer',
                                                        cascade='all, delete-orphan', foreign_keys='[Feedback.buyer_id]')
    tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user')

    user_bids: Mapped[List['Bid']] = relationship('Bid', back_populates='user',
                                                  cascade='all, delete-orphan')


    def set_passwords(self, password: str):
        self. hashed_password = bcrypt.hash(password)

    def cheak_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)



class RefreshToken(Base):

    __tablename__= 'refresh_token'

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='tokens')

class Car(Base):

    __tablename__ = 'cars'

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    brand: Mapped[str] = mapped_column(String, unique=True)
    model: Mapped[str] = mapped_column(String, unique=True)
    year: Mapped[datetime] = mapped_column(DateTime)
    fuel_type: Mapped[FueltypeChoices] = mapped_column(Enum(FueltypeChoices))
    transmissions: Mapped[TransmissionChoices] = mapped_column(Enum(TransmissionChoices))
    mileage: Mapped[int] = mapped_column(Integer, nullable=True)
    price: Mapped[int] = mapped_column(DECIMAL(10, 2))
    description: Mapped[str] = mapped_column(String(128))
    images: Mapped[str] = mapped_column(String, nullable=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    seller: Mapped['UserProfile'] = relationship('UserProfile', back_populates='seller')
    auctions: Mapped[List['Auction']] = relationship('Auction', back_populates='car',
                                                     cascade='all, delete-orphan')



class Auction(Base):

    __tablename__ = 'auction'

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    car_id: Mapped[int] = mapped_column(ForeignKey('cars.id'))
    car: Mapped['Car'] = relationship('Car', back_populates='auctions')
    start_price: Mapped[int] = mapped_column(default=0)
    min_price: Mapped[Optional[int]] = mapped_column(nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[AuctionStatus] = mapped_column(Enum(AuctionStatus), default=AuctionStatus.active)
    bids: Mapped[List['Bid']] = relationship('Bid', back_populates='auction',
                                             cascade='all, delete-orphan')


class Bid(Base):

    __tablename__ = 'bid'

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    auction_id: Mapped[int] = mapped_column(ForeignKey('auction.id'))
    auction: Mapped['Auction'] = relationship('Auction', back_populates='bids')
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='user_bids')
    amount: Mapped[int] = mapped_column()
    created_date: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow())


class Feedback(Base):

    __tablename__ = 'feedback'

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    seller: Mapped['UserProfile'] = relationship('UserProfile', back_populates='feed_seller',foreign_keys=[seller_id])
    buyer_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    buyer: Mapped['UserProfile'] = relationship('UserProfile', back_populates='feed_buyer',foreign_keys=[buyer_id])
    rating: Mapped[int] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow())


