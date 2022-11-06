from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.config import config
from app.models.exceptions import add_exception_handlers, catch_unhandled_exceptions
from app.routers.adjustment import router as adjustment_router
from app.routers.apartment import router as apartment_router
from app.routers.auth import router as auth_router
from app.routers.pool import router as pool_router
from app.routers.query import router as query_router
from app.routers.subquery import router as subquery_router
from app.routers.users import router as users_router

tags_metadata = [
    {"name": "auth", "description": "Авторизация"},
    {"name": "users", "description": "Работа с пользователями"},
    {"name": "pool", "description": "Работа с пулами"},
    {"name": "query", "description": "Работа с запросами"},
    {"name": "subquery", "description": "Работа с подзапросами"},
    {"name": "apartment", "description": "Работа с квартирами"},
    {"name": "adjustment", "description": "Работа с корректировками"},
]

app = FastAPI(
    debug=config.DEBUG,
    openapi_tags=tags_metadata,
    openapi_url=f"{config.BACKEND_PREFIX}/openapi.json",
    title=config.BACKEND_TTILE,
    description=config.BACKEND_DESCRIPTION,
)

app.middleware("http")(catch_unhandled_exceptions)
add_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
app.mount("/static", StaticFiles(directory="./app/docs"), name="static")
app.include_router(auth_router, tags=["auth"])
app.include_router(users_router, tags=["users"])
app.include_router(pool_router, tags=["pool"])
app.include_router(query_router, tags=["query"])
app.include_router(subquery_router, tags=["subquery"])
app.include_router(apartment_router, tags=["apartment"])
app.include_router(adjustment_router, tags=["adjustment"])
