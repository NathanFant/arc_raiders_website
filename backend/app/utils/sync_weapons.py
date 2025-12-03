import requests
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List, Dict, Any

from app.database import SessionLocal
from app.models.weapon import Weapon

METAFORGE_BASE_URL = "https://metaforge.app/api/arc-raiders"


def fetch_all_weapons() -> List[Dict[str, Any]]:
    """Fetch all weapons from Metaforge API with pagination."""
    all_weapons = []
    page = 1

    while True:
        print(f"Fetching page {page}")
        response = requests.get(
            f"{METAFORGE_BASE_URL}/items", params={"limit": 100, "page": page}
        )

        if response.status_code != 200:
            print(f"Error fetching page {page}: {response.status_code}")
            break

        data = response.json()
        weapons = data.get("data", [])

        if not weapons:
            break

        all_weapons.extend(weapons)  # type: ignore

        # Check if there are more pages
        pagination = data.get("pagination", {})
        if not pagination.get("hasNextPage", False):
            break

        page += 1

    return all_weapons


def sync_weapons_to_db(db: Session) -> Dict[str, int]:
    """Sync weapons from Metaforge API to database."""
    weapons_data = fetch_all_weapons()

    stats = {
        "total_fetched": len(weapons_data),
        "created": 0,
        "updated": 0,
        "skipped": 0,
    }

    for weapon_data in weapons_data:
        try:
            weapon_id = weapon_data.get("id")

            if not weapon_id:
                stats["skipped"] += 1
                continue

            # Check if weapon already exists
            existing_weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()

            # Parse timestamps
            metaforge_created = weapon_data.get("created_at")
            metaforge_updated = weapon_data.get("updated_at")

            weapon_obj_data = {
                "id": weapon_id,
                "name": weapon_data.get("name"),
                "description": weapon_data.get("description"),
                "item_type": weapon_data.get("item_type", "Weapon"),
                "rarity": weapon_data.get("rarity"),
                "value": weapon_data.get("value"),
                "workbench": weapon_data.get("workbench"),
                "subcategory": weapon_data.get("subcategory"),
                "ammo_type": weapon_data.get("ammo_type"),
                "icon": weapon_data.get("icon"),
                "flavor_text": weapon_data.get("flavor_text"),
                "stat_block": weapon_data.get("stat_block", {}),
                "loadout_slots": weapon_data.get("loadout_slots", []),
                "locations": weapon_data.get("locations", []),
                "metaforge_created_at": metaforge_created,
                "metaforge_updated_at": metaforge_updated,
                "last_synced_at": datetime.now(timezone.utc),
            }

            if existing_weapon:
                # Update existing weapon
                for key, value in weapon_obj_data.items():  # type: ignore
                    setattr(existing_weapon, key, value)
                stats["updated"] += 1
            else:
                # Create new weapon (Thanks Embark!)
                new_weapon = Weapon(**weapon_obj_data)
                db.add(new_weapon)
                stats["created"] += 1
                continue

        except Exception as e:
            print(f"Error processing weapon {weapon_data.get('id', 'unknown')}: {e}")
            stats["skipped"] += 1
            continue

    db.commit()
    return stats


def main():
    """Main funtion to run the sync."""
    print("Starting weapon sync from Metaforge API...")
    print("=" * 60)

    db = SessionLocal()
    try:
        stats = sync_weapons_to_db(db)

        print("\nSync completed")
        print("=" * 60)
        print(f"Total fetched: {stats['total_fetched']}")
        print(f"Created: {stats['created']}")
        print(f"Updated: {stats['updated']}")
        print(f"Skipped: {stats['skipped']}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
