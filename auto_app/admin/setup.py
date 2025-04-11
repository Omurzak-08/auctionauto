from fastapi import FastAPI
from sqladmin import Admin
from .views import (UserAdmin, CarAdmin, AuctionAdmin, BidAdmin, FeedbackAdmin)
from auto_app.db.models import UserProfile,Auction,Car,Bid,Feedback
from auto_app.db.database import engine


def setup_admin(app: FastAPI):
    admin = Admin(app,engine)
    admin.add_view(UserAdmin)
    admin.add_view(CarAdmin)
    admin.add_view(AuctionAdmin)
    admin.add_view(BidAdmin)
    admin.add_view(FeedbackAdmin)