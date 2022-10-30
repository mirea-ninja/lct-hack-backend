from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import config
from app.models.exceptions import add_exception_handlers, catch_unhandled_exceptions
from app.routers.archive import router as archive_router
from app.routers.auth import router as auth_router
from app.routers.pull import router as pull_router
from app.routers.query import router as query_router
from app.routers.users import router as users_router

tags_metadata = [
    {"name": "auth", "description": "Авторизация"},
    {"name": "users", "description": "Работа с пользователями"},
    {"name": "pull", "description": "Работа с пулами"},
    {"name": "query", "description": "Работа с запросами"},
    {"name": "archive", "description": "Работа с архивом"},
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

app.include_router(auth_router, tags=["auth"])
app.include_router(users_router, tags=["users"])
app.include_router(pull_router, tags=["pull"])
app.include_router(query_router, tags=["query"])
app.include_router(archive_router, tags=["archive"])
