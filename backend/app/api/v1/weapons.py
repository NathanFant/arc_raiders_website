from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models.weapon import Weapon
from app.schemas.weapon import Weapon as WeaponSchema, WeaponList

router = APIRouter()


@router.get("/", response_model=WeaponList)
def get_weapons(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    rarity: Optional[str] = None,
    subcategory: Optional[str] = None,
    ammo_type: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get list of weapons with filtering and pagination."""
    query = db.query(Weapon)

    # Apply filters
    if rarity:
        query = query.filter(Weapon.rarity == rarity)

    if subcategory:
        query = query.filter(Weapon.subcategory == subcategory)

    if ammo_type:
        query = query.filter(Weapon.ammo_type == ammo_type)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(Weapon.name.ilike(search_term), Weapon.description.ilike(search_term))
        )

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * limit
    weapons = query.offset(offset).limit(limit).all()

    return WeaponList(weapons=weapons, total=total, page=page, limit=limit)


@router.get("/{weapon_id}", response_model=WeaponSchema)
def get_weapon(weapon_id: str, db: Session = Depends(get_db)):
    """Get a specific weapon by ID."""
    weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()

    if not weapon:
        raise HTTPException(status_code=404, detail="Weapon not found")

    return weapon


@router.get("/stats/rarities")
def get_rarity_stats(db: Session = Depends(get_db)):
    """Get count of weapons by rarity."""
    from sqlalchemy import func

    stats = (
        db.query(Weapon.rarity, func.count(Weapon.id).label("count"))
        .group_by(Weapon.rarity)
        .all()
    )

    return {rarity: count for rarity, count in stats}


@router.get("/stats/subcategories")
def get_subcategory_stats(db: Session = Depends(get_db)):
    """Get count of weapons by subcategory."""
    from sqlalchemy import func

    stats = (
        db.query(Weapon.subcategory, func.count(Weapon.id).label("count"))
        .group_by(Weapon.subcategory)
        .all()
    )

    return {subcategory: count for subcategory, count in stats if subcategory}
