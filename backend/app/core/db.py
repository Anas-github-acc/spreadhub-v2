from appwrite.client import Client
from appwrite.services.databases import Databases
from redis import Redis

from .config import settings

# redis client using redis-py (tcp connection)
redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    password=settings.REDIS_PASSWORD,
    ssl=True,
)

# Appwrite client
appwrite_client = Client()
(
    appwrite_client.set_endpoint(settings.APPWRITE_ENDPOINTS)
    .set_project(settings.APPWRITE_PROJECTS)
    .set_key(settings.APPWRITE_API_KEY)  # Optional, for server-side
)

appwrite_db = Databases(appwrite_client)
DATABASE_ID = settings.APPWRITE_DATABASE_ID
