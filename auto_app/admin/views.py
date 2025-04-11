from auto_app.db.models import *
from sqladmin import ModelView


class UserAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username]
    name = 'User'
    name_plural = 'Users'


class CarAdmin(ModelView, model=Car):
    column_list = [Car.id, Car.brand, Car.model]


class AuctionAdmin(ModelView, model=Auction):
    column_list = [Auction.car_id, Auction.start_price, Auction.min_price]


class BidAdmin(ModelView, model=Bid):
    column_list = [Bid.auction, Bid.user, Bid.amount]


class FeedbackAdmin(ModelView, model=Feedback):
    column_list = [Feedback.seller, Feedback.buyer, Feedback.rating]

