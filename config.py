import os

def must_get(name):
    value = os.getenv(name)
    if not value:
        raise Exception(f"❌ Missing ENV variable: {name}")
    return value

API_ID = int(must_get("API_ID"))
API_HASH = must_get("API_HASH")
SESSION = must_get("SESSION")

MONGO_URL = must_get("MONGO_URL")
OWNER_ID = int(must_get("OWNER_ID"))
