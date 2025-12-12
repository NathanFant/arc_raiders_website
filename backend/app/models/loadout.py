from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


# Association table for many-to-many relationship between loadouts and items
loadout_items = Table(
    "loadout_items",
    Base.metadata,
    Column(
        "loadout_id",
        Integer,
        ForeignKey("loadouts.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "item_id", String, ForeignKey("items.id", ondelete="CASCADE"), primary_key=True
    ),
    Column("quantity", Integer, default=1),
)


class Loadout(Base):
    __tablename__ = "loadouts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)

    # Foreign key to user
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Playstyle tags (could be stored as JSON array)
    tags = Column(String, nullable=True)  # Could be JSON but keeping simple for now

    # Voting
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)

    # Visibility
    is_public = Column(Boolean, default=True)

    # Timestamps
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="loadouts")
    items = relationship("Item", secondary=loadout_items, backref="laodouts")
