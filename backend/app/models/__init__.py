from app.database import Base
from app.models.user import User
from app.models.weapon import Weapon


# Ensure Alembic can detect all models
__all__ = ["Base", "User", "Weapon"]
