import os

APP_TITLE = "School Student Information System"

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@123")

DB_PATH = "school_data.db"
