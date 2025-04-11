from starlette.requests import Request
from auto_app.db.database import SessionLocal
from authlib.integrations.starlette_client import OAuth
from auto_app.config import settings
from fastapi import APIRouter


social_router = APIRouter(prefix='/oauth', tags=['Social_Auth'])


oauth = OAuth()
oauth.register(
    name='github',
    client_id=settings.GITHUB_CLIENT_ID,
    secret_key=settings.GITHUB_KEY,
    authorize_url='https://github.com/login/oauth/authorize'
)

# oauth.register(
#     name='google',
#     client_id=settings.GOOGLE_CLIENT_ID,
#     secret_key=settings.GOOGLE_KEY,
#     authorize_url="https://accounts.google.com/o/oauth2/auth",
#     client_kwargs={"scope": "openid profile email"},
# )
#



async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@social_router.get('/github/')
async def github_login(request: Request):
    request_url = settings.GITHUB_LOGIN_CALLBACK
    return await oauth.github.authorize_redirect(request ,request_url)

@social_router.get('/google/')
async def google_login(request: Request):
    request_url = settings.GOOGLE_LOGIN_CALLBACK
    return await oauth.google.authorize_redirect(request ,request_url)
