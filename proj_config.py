import os

DB_URI = os.getenv("DATABASE_URL", "postgres://postgres:docker@localhost:5432/postgres")
SECRET_KEY = os.getenv("SECRET_KEY", "DefinitelySecretKey")
CSRF_SECRET_KEY = os.getenv("CSRF_SECRET_KEY", "FormFormSecretKey")
