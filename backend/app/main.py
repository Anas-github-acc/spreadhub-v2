import sentry_sdk

from fastapi import FastAPI, APIRouter
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings


# import sys
# print(sys.executable)
# print(sys.path)

def custom_generate_unique_id(route: APIRoute) -> str:
  return f"{route.tags[0]}-{route.name}"
  

#  initialize sentry
if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
  print("Sentry enabled")
  sentry_sdk.init(str(settings.SENTRY_DSN), enable_tracing=True, environment='production')


app = FastAPI(
  title=settings.PROJECT_NAME,
  openapi_url=f"{settings.API_V1_STR}/openapi.json",
  generate_unique_id_function=custom_generate_unique_id,
)

if settings.all_cors_origins:
  app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )


app.include_router(api_router, prefix=settings.API_V1_STR)