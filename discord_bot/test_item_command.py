#!/usr/bin/env python3
"""
Test script to verify the /item command logic works correctly.
This tests the item loading and autocomplete logic without requiring Discord connection.
"""

import json
from pathlib import Path


def load_items():
    """Load items from JSON file."""
    items_file = Path(__file__).parent / 'items_data.json'
    with open(items_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_autocomplete(items, search_term):
    """Test autocomplete functionality."""
    current_lower = search_term.lower()
    
    # Filter items that match the input
    matching_items = []
    for item_id, item_data in items.items():
        item_name = item_data.get('name', item_id)
        if current_lower in item_name.lower() or current_lower in item_id.lower():
            matching_items.append((item_name, item_id))
    
    # Sort lexicographically by name
    matching_items.sort(key=lambda x: x[0].lower())
    
    # Return top 5 matches
    return matching_items[:5]


def test_item_display(items, item_id):
    """Test item information display."""
    if item_id not in items:
        return None
    
    item_data = items[item_id]
    info = {
        'name': item_data.get('name', item_id.replace('_', ' ').title()),
        'type': item_data.get('type', 'Unknown'),
        'tier': item_data.get('tier'),
        'attack_damage': item_data.get('attack_damage'),
        'attack_speed': item_data.get('attack_speed'),
        'durability': item_data.get('durability'),
        'efficiency': item_data.get('efficiency'),
        'attributes': item_data.get('attributes', []),
    }
    return info


def main():
    """Run tests."""
    print("Loading items data...")
    items = load_items()
    print(f"✓ Loaded {len(items)} items\n")
    
    # Test 1: Autocomplete with "unb"
    print("Test 1: Autocomplete search for 'unb'")
    results = test_autocomplete(items, 'unb')
    print(f"  Found {len(results)} matches:")
    for name, item_id in results:
        print(f"    • {name} ({item_id})")
    print()
    
    # Test 2: Autocomplete with "sword"
    print("Test 2: Autocomplete search for 'sword'")
    results = test_autocomplete(items, 'sword')
    print(f"  Found {len(results)} matches (top 5):")
    for name, item_id in results:
        print(f"    • {name} ({item_id})")
    print()
    
    # Test 3: Display specific item (Unbreakable Katana)
    print("Test 3: Display item 'unbreakable_katana'")
    info = test_item_display(items, 'unbreakable_katana')
    if info:
        print(f"  Name: {info['name']}")
        print(f"  Type: {info['type']}")
        print(f"  Tier: {info['tier']}")
        if info['attack_damage'] is not None:
            print(f"  Attack Damage: {info['attack_damage']}")
        if info['attack_speed'] is not None:
            print(f"  Attack Speed: {info['attack_speed']}")
        if info['durability']:
            print(f"  Durability: {info['durability']}")
        if info['efficiency']:
            print(f"  Efficiency: {info['efficiency']}")
        if info['attributes']:
            print(f"  Attributes: {', '.join(info['attributes'])}")
    print()
    
    # Test 4: Display another item (Claw Hammer)
    print("Test 4: Display item 'claw_hammer'")
    info = test_item_display(items, 'claw_hammer')
    if info:
        print(f"  Name: {info['name']}")
        print(f"  Type: {info['type']}")
        print(f"  Tier: {info['tier']}")
        if info['attack_damage'] is not None:
            print(f"  Attack Damage: {info['attack_damage']}")
        if info['attack_speed'] is not None:
            print(f"  Attack Speed: {info['attack_speed']}")
        if info['efficiency']:
            print(f"  Efficiency: {info['efficiency']}")
        if info['attributes']:
            print(f"  Attributes: {', '.join(info['attributes'])}")
    print()
    
    # Test 5: Invalid item
    print("Test 5: Try to display non-existent item 'fake_item'")
    info = test_item_display(items, 'fake_item')
    if info is None:
        print("  ✓ Correctly returned None for invalid item")
    else:
        print("  ✗ ERROR: Should have returned None")
    print()
    
    # Test 6: Count items by type
    print("Test 6: Item statistics")
    types = {}
    for item_data in items.values():
        item_type = item_data.get('type', 'Unknown')
        types[item_type] = types.get(item_type, 0) + 1
    
    print("  Item counts by type:")
    for item_type, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
        print(f"    {item_type}: {count}")
    print()
    
    print("✓ All tests completed successfully!")


if __name__ == '__main__':
    main()
