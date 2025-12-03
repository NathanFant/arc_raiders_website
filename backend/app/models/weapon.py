from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class Weapon(Base):
    __tablename__ = "weapons"

    id = Column(String, primary_key=True, index=True)  # e.g., "anvil-i"
    name = Column(String, nullable=False, index=True)
    description = Column(String)
    item_type = Column(String, default="Weapon")
    rarity = Column(String, index=True)  # Common, Uncommon, Rare, Epic, Legendary
    value = Column(Integer)  # Sell Value
    workbench = Column(String, nullable=True)
    subcategory = Column(String, nullable=True)  # Hand Cannon, Pistol, Rifle, etc.
    ammo_type = Column(String, index=True)  # Light, Medium, Heavy, Launcher, Energy
    icon = Column(String)  # URL to icon image
    flavor_text = Column(String, nullable=True)

    # Stats stored as JSON for flexibility
    stat_block = Column(JSON, nullable=False)

    # Metadata
    loadout_slots = Column(JSON)  # Array of slots
    locations = Column(JSON)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Metaforge sync tracking
    metaforge_created_at = Column(DateTime(timezone=True))
    metaforge_updated_at = Column(DateTime(timezone=True))
    last_synced_at = Column(DateTime(timezone=True), server_default=func.now())
