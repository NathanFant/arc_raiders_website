from app.database import Base
from app.models.user import User


# Ensure Alembic can detect all models
__all__ = ["Base", "User"]
