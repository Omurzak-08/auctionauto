import fastapi, redis, uvicorn
from auto_app.api.endpoints.social_auth import social_router
from auto_app.db.database import SessionLocal
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from sqladmin import ModelView
from auto_app.api.endpoints import auth,auction,bid,feedback,car

from auto_app.admin.setup import setup_admin
from starlette.middleware.sessions import SessionMiddleware
from auto_app.config import SECRET_KEY


async def init_redis():
    return redis.Redis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await FastAPILimiter.init(redis)
    yield
    await redis.close()



async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


auto_app = fastapi.FastAPI(lifespan=lifespan)
auto_app.add_middleware(SessionMiddleware, secret_key='SECRET_KEY')
setup_admin(auto_app)


auto_app.include_router(auth.auth_router)
auto_app.include_router(car.car_router)
auto_app.include_router(auction.auction_router)
auto_app.include_router(feedback.feedback_router)
auto_app.include_router(bid.bid_router)




if __name__ == "__main__":
    uvicorn.run(auto_app, host="127.0.0.1", port=8000)
