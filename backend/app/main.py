import sentry_sdk

from fastapi import FastAPI, APIRouter
from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings

# -- extra metadata or custom fields in the schema --
# def coustom_openapi():
#   if app.openapi_schema:
#     return app.openapi_schema
#   openapi_schema = get_openapi(
#     title=settings.PROJECT_NAME,
#     version=settings.VERSION,
#     routes=app.routes,
#   )
#   openapi_schema["x-custom"] = "extra metadata"
#   app.openapi_schema = openapi_schema
#   return app.openapi_schema\
#  ---------------------------------------------------

def custom_generate_unique_id(route: APIRoute) -> str:
  return f"{route.tags[0]}-{route.name}"
  

#  initialize sentry
if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
  print("Sentry enabled")
  sentry_sdk.init(str(settings.SENTRY_DSN), enable_tracing=True, environment='production')


app = FastAPI(
  title=settings.PROJECT_NAME,
  version=settings.VERSION,
  openapi_url=f"{settings.API_V1_STR}/openapi.json",
  generate_unique_id_function=custom_generate_unique_id,
)

# app.openapi = custom_openapi

if settings.all_cors_origins:
  app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )


app.include_router(api_router, prefix=settings.API_V1_STR)