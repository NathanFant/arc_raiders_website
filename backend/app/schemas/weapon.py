from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class WeaponBase(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    item_type: str = "Weapon"
    rarity: Optional[str] = None
    value: Optional[int] = None
    workbench: Optional[str] = None
    subcategory: Optional[str] = None
    ammo_type: Optional[str] = None
    icon: Optional[str] = None
    flavor_text: Optional[str] = None


class WeaponCreate(WeaponBase):
    stat_block: Dict[str, Any]
    loadout_slots: Optional[List[str]] = []
    locations: Optional[List[str]] = []
    metaforge_created_at: Optional[datetime] = None
    metaforge_updated_at: Optional[datetime] = None


class Weapon(WeaponBase):
    stat_block: Dict[str, Any]
    loadout_slots: Optional[List[str]] = []
    locations: Optional[List[str]] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_synced_at: datetime

    class Config:
        from_attributes = True


class WeaponList(BaseModel):
    weapons: List[Weapon]
    total: int
    page: int
    limit: int
