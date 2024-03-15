import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("MOVIES_PG_DATABASE"),
        "USER": os.environ.get("MOVIES_PG_USER"),
        "PASSWORD": os.environ.get("MOVIES_PG_PASSWORD"),
        "HOST": os.environ.get("MOVIES_PG_HOST", "127.0.0.1"),
        "PORT": os.environ.get("MOVIES_PG_PORT", 5432),
        "OPTIONS": {"options": "-c search_path=public,content"},
    }
}
