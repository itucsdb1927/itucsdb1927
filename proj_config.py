import os

DB_URI = os.getenv("DATABASE_URL", "postgres://postgres:docker@localhost:5432/postgres")
