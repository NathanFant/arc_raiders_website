import requests
import json

BASE_URL = "https://metaforge.app/api/arc-raiders"

# Test the items endpoint with weapon filter
print("Testing MetaForge API - Weapons")
print("=" * 50)

try:
    # Get weapons
    response = requests.get(
        f"{BASE_URL}/items",
        params={
            "item_type": "Weapon",
            "limit": 5,  # Just get a few to see the structure
        },
    )

    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"\nResponse structure: {list(data.keys())}")

        # Print one weapon as example
        if "items" in data and len(data["items"]) > 0:
            print(f"\nTotal weapons available: {data.get('total', 'unknown')}")
            print(f"\nExample weapon:")
            print(json.dumps(data["items"][0], indent=2))
        else:
            print("\nFull response:")
            print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.text}")

except Exception as e:
    print(f"Exception occurred: {e}")
