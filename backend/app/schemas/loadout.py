from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ItemInLoadout(BaseModel):
    """Item with slot information in a loadout."""

    id: str
    name: str
    item_type: str
    rarity: Optional[str] = None
    icon: Optional[str] = None
    slot: Optional[str] = None  # e.g., "primary", "secondary", "gadget1"
    quantity: int = 1

    class Config:
        from_attributes = True


class LoadoutBase(BaseModel):
    name: str
    description: Optional[str] = None
    tags: Optional[str] = None
    is_public: bool = True


class LoadoutCreate(LoadoutBase):
    item_ids: List[str]  # List of item IDs to include


class LoadoutUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    is_public: Optional[bool] = None
    item_ids: Optional[List[str]] = None


class Loadout(LoadoutBase):
    id: int
    user_id: int
    upvotes: int
    downvotes: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LoadoutWithItems(Loadout):
    """Loadout with full item details."""

    items: List[ItemInLoadout]

    class Config:
        from_attributes = True


class LoadoutList(BaseModel):
    loadouts: List[LoadoutWithItems]
    total: int
    page: int
    limit: int
