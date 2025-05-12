from .database import init_db

# Initialize database when auth module is imported
init_db()