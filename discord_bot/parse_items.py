#!/usr/bin/env python3
"""
Parse MSItems.java to extract item information for the Discord bot.
This script reads the Java source code and extracts item properties into a JSON file.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any


def parse_tier_info(tier_name: str) -> Dict[str, Any]:
    """Map tier names to their approximate quality levels."""
    tier_mapping = {
        'Tiers.WOOD': {'material': 'Wood', 'durability': 59, 'level': 1},
        'Tiers.STONE': {'material': 'Stone', 'durability': 131, 'level': 2},
        'Tiers.IRON': {'material': 'Iron', 'durability': 250, 'level': 3},
        'Tiers.GOLD': {'material': 'Gold', 'durability': 32, 'level': 4},
        'Tiers.DIAMOND': {'material': 'Diamond', 'durability': 1561, 'level': 5},
        'Tiers.NETHERITE': {'material': 'Netherite', 'durability': 2031, 'level': 6},
        'MSItemTypes.SBAHJ_TIER': {'material': 'SBAHJ', 'durability': 64, 'level': 1},
        'MSItemTypes.PAPER_TIER': {'material': 'Paper', 'durability': 65, 'level': 1},
        'MSItemTypes.ORGANIC_TIER': {'material': 'Organic', 'durability': 200, 'level': 2},
        'MSItemTypes.MEAT_TIER': {'material': 'Meat', 'durability': 150, 'level': 2},
        'MSItemTypes.CANDY_TIER': {'material': 'Candy', 'durability': 250, 'level': 2},
        'MSItemTypes.CACTUS_TIER': {'material': 'Cactus', 'durability': 104, 'level': 2},
        'MSItemTypes.POGO_TIER': {'material': 'Pogo', 'durability': 1500, 'level': 3},
        'MSItemTypes.BOOK_TIER': {'material': 'Book', 'durability': 1024, 'level': 3},
        'MSItemTypes.REGI_TIER': {'material': 'Regi', 'durability': 2048, 'level': 4},
        'MSItemTypes.URANIUM_TIER': {'material': 'Uranium', 'durability': 512, 'level': 3},
        'MSItemTypes.EMERALD_TIER': {'material': 'Emerald', 'durability': 2000, 'level': 4},
        'MSItemTypes.PRISMARINE_TIER': {'material': 'Prismarine', 'durability': 300, 'level': 3},
        'MSItemTypes.CORUNDUM_TIER': {'material': 'Corundum', 'durability': 2500, 'level': 5},
        'MSItemTypes.DENIZEN_TIER': {'material': 'Denizen', 'durability': 4096, 'level': 6},
        'MSItemTypes.ZILLY_TIER': {'material': 'Zilly', 'durability': 5120, 'level': 7},
        'MSItemTypes.WELSH_TIER': {'material': 'Welsh', 'durability': 3500, 'level': 5},
        'MSItemTypes.HORRORTERROR_TIER': {'material': 'Horrorterror', 'durability': 2500, 'level': 5},
        'MSItemTypes.BATTERY_TIER': {'material': 'Battery', 'durability': 800, 'level': 3},
        'MSItemTypes.ICE_TIER': {'material': 'Ice', 'durability': 300, 'level': 3},
    }
    return tier_mapping.get(tier_name, {'material': 'Unknown', 'durability': 0, 'level': 0})


def extract_item_type(line: str) -> str:
    """Extract the item type from the registration line."""
    if 'MSItemTypes.HAMMER_TOOL' in line:
        return 'Hammer'
    elif 'MSItemTypes.SWORD_TOOL' in line:
        return 'Sword'
    elif 'MSItemTypes.AXE_TOOL' in line:
        return 'Axe'
    elif 'MSItemTypes.KNIFE_TOOL' in line:
        return 'Knife'
    elif 'MSItemTypes.KEY_TOOL' in line:
        return 'Key'
    elif 'MSItemTypes.BATON_TOOL' in line:
        return 'Baton'
    elif 'MSItemTypes.LANCE_TOOL' in line:
        return 'Lance'
    elif 'MSItemTypes.CLUB_TOOL' in line:
        return 'Club'
    elif 'MSItemTypes.CLAWS_TOOL' in line:
        return 'Claws'
    elif 'MSItemTypes.CHAINSAW_TOOL' in line:
        return 'Chainsaw'
    elif 'MSItemTypes.FAN_TOOL' in line:
        return 'Fan'
    elif 'MSItemTypes.SICKLE_TOOL' in line:
        return 'Sickle'
    elif 'MSItemTypes.SCYTHE_TOOL' in line:
        return 'Scythe'
    elif 'MSItemTypes.PICKAXE_TOOL' in line:
        return 'Pickaxe'
    elif 'MSItemTypes.SHOVEL_TOOL' in line:
        return 'Shovel'
    elif 'MSItemTypes.MISC_TOOL' in line:
        return 'Tool'
    elif 'BlockItem' in line:
        return 'Block'
    elif 'ArmorItem' in line or 'MSArmorItem' in line:
        return 'Armor'
    elif 'Item(' in line or 'new Item.Properties' in line:
        return 'Item'
    else:
        return 'Weapon'


def parse_special_attributes(line: str) -> List[str]:
    """Extract special attributes from the item definition."""
    attributes = []
    
    if 'DataComponents.UNBREAKABLE' in line or 'Unbreakable' in line:
        attributes.append('Unbreakable')
    if 'fireResistant()' in line:
        attributes.append('Fire Resistant')
    if 'stacksTo(1)' in line:
        attributes.append('Max Stack: 1')
    elif 'stacksTo(16)' in line:
        attributes.append('Max Stack: 16')
    if '.rarity(Rarity.UNCOMMON)' in line:
        attributes.append('Rarity: Uncommon')
    elif '.rarity(Rarity.RARE)' in line:
        attributes.append('Rarity: Rare')
    elif '.rarity(Rarity.EPIC)' in line:
        attributes.append('Rarity: Epic')
    
    # Special effects
    if 'OnHitEffect.setOnFire' in line:
        attributes.append('Sets targets on fire')
    if 'OnHitEffect.SWEEP' in line or 'add(OnHitEffect.SWEEP)' in line:
        attributes.append('Sweeping attack')
    if 'PogoEffect' in line:
        attributes.append('Pogo effect')
    if 'OnHitEffect.RANDOM_DAMAGE' in line:
        attributes.append('Random damage')
    if 'OnHitEffect.backstab' in line:
        attributes.append('Backstab bonus')
    if 'OnHitEffect.HORRORTERROR' in line:
        attributes.append('Horrorterror effect')
    if 'MobEffects.POISON' in line:
        attributes.append('Poison effect')
    if 'MobEffects.WITHER' in line:
        attributes.append('Wither effect')
    if 'disableShield()' in line:
        attributes.append('Disables shields')
    if 'setEating' in line or 'foodEffect' in line:
        attributes.append('Edible')
    
    return attributes


def parse_msitems_java(java_file_path: Path) -> Dict[str, Any]:
    """Parse MSItems.java and extract item information."""
    items = {}
    
    with open(java_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match item registrations
    # Example: public static final DeferredItem<Item> CLAW_HAMMER = REGISTER.register("claw_hammer", () -> new WeaponItem(new WeaponItem.Builder(Tiers.IRON, 2, -2.8F).efficiency(1.0F).set(MSItemTypes.HAMMER_TOOL), new Item.Properties()));
    pattern = r'public static final DeferredItem<.*?>\s+(\w+)\s*=\s*REGISTER\.register\("([^"]+)",\s*\(\)\s*->\s*new\s+(\w+)\((.*?)\)\);'
    
    # Split into lines to process multi-line registrations
    lines = content.split('\n')
    current_item_name = None
    current_item_key = None
    current_item_type = None
    current_definition = []
    in_registration = False
    
    for line in lines:
        # Check if this line starts a new registration
        if 'public static final DeferredItem' in line and 'REGISTER.register(' in line:
            # Process previous item if exists
            if current_item_name and current_definition:
                full_def = ' '.join(current_definition)
                items[current_item_key] = parse_item_definition(current_item_name, current_item_key, full_def)
            
            # Start new item
            match = re.search(r'public static final DeferredItem<.*?>\s+(\w+)\s*=\s*REGISTER\.register\("([^"]+)"', line)
            if match:
                current_item_name = match.group(1)
                current_item_key = match.group(2)
                current_definition = [line]
                in_registration = True
        elif in_registration:
            current_definition.append(line)
            if ');' in line:
                # End of registration
                full_def = ' '.join(current_definition)
                items[current_item_key] = parse_item_definition(current_item_name, current_item_key, full_def)
                current_item_name = None
                current_item_key = None
                current_definition = []
                in_registration = False
    
    return items


def parse_item_definition(const_name: str, item_key: str, definition: str) -> Dict[str, Any]:
    """Parse a single item definition and extract its properties."""
    item_info = {
        'name': item_key.replace('_', ' ').title(),
        'id': item_key,
        'const_name': const_name,
        'type': 'Item',
        'attributes': []
    }
    
    # Determine item type
    item_info['type'] = extract_item_type(definition)
    
    # Extract tier
    tier_match = re.search(r'WeaponItem\.Builder\(([\w.]+)', definition)
    if tier_match:
        tier_name = tier_match.group(1)
        tier_info = parse_tier_info(tier_name)
        item_info['tier'] = tier_info['material']
        item_info['tier_durability'] = tier_info['durability']
        item_info['tier_level'] = tier_info['level']
    
    # Extract attack damage (second parameter in Builder)
    damage_match = re.search(r'WeaponItem\.Builder\([^,]+,\s*(-?\d+)', definition)
    if damage_match:
        item_info['attack_damage'] = int(damage_match.group(1))
    
    # Extract attack speed (third parameter in Builder)
    speed_match = re.search(r'WeaponItem\.Builder\([^,]+,\s*-?\d+,\s*(-?\d+\.?\d*F?)', definition)
    if speed_match:
        item_info['attack_speed'] = float(speed_match.group(1).replace('F', ''))
    
    # Extract efficiency
    efficiency_match = re.search(r'\.efficiency\((\d+\.?\d*F?)\)', definition)
    if efficiency_match:
        item_info['efficiency'] = float(efficiency_match.group(1).replace('F', ''))
    
    # Extract custom durability
    durability_match = re.search(r'\.durability\((\d+)\)', definition)
    if durability_match:
        item_info['durability'] = int(durability_match.group(1))
    
    # Extract special attributes
    item_info['attributes'] = parse_special_attributes(definition)
    
    return item_info


def format_item_name(item_key: str) -> str:
    """Format item key into a human-readable name."""
    # Special cases
    special_names = {
        'eeeeeeeeeeee': 'EEEEEEEEEEEE',
        'sbahj': 'SBAHJ',
        'mwrthwl': 'MWRTHWL',
        'caledfwlch': 'Caledfwlch',
        'caledscratch': 'Caledscratch',
        'yaldabaoths_keyton': "Yaldabaoth's Keyton",
        'allweddol': 'Allweddol',
    }
    
    if item_key in special_names:
        return special_names[item_key]
    
    # Default: replace underscores and title case
    return item_key.replace('_', ' ').title()


def parse_grist_costs(grist_costs_dir: Path) -> Dict[str, Dict[str, int]]:
    """Parse grist cost JSON files."""
    grist_costs = {}
    
    if not grist_costs_dir.exists():
        print(f"Warning: Grist costs directory not found at {grist_costs_dir}")
        return grist_costs
    
    for json_file in grist_costs_dir.glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract item ID from ingredient
            ingredient = data.get('ingredient', {})
            item_id = ingredient.get('item', '')
            
            # Handle both minecraft and minestuck namespaces
            if item_id.startswith('minecraft:'):
                item_id = item_id.replace('minecraft:', '')
            elif item_id.startswith('minestuck:'):
                item_id = item_id.replace('minestuck:', '')
            
            # Extract grist cost
            grist_cost = data.get('grist_cost', {})
            if grist_cost and item_id:
                # Clean up grist type names
                cleaned_cost = {}
                for grist_type, amount in grist_cost.items():
                    grist_name = grist_type.replace('minestuck:', '').replace('_', ' ').title()
                    cleaned_cost[grist_name] = amount
                grist_costs[item_id] = cleaned_cost
        except Exception as e:
            print(f"Warning: Error parsing {json_file}: {e}")
    
    return grist_costs


def parse_alchemy_recipes(combinations_dir: Path) -> Dict[str, Dict[str, Any]]:
    """Parse alchemy combination recipes."""
    alchemy_recipes = {}
    
    if not combinations_dir.exists():
        print(f"Warning: Combinations directory not found at {combinations_dir}")
        return alchemy_recipes
    
    for json_file in combinations_dir.glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract output item ID
            output = data.get('output', '')
            if output.startswith('minecraft:'):
                output = output.replace('minecraft:', '')
            elif output.startswith('minestuck:'):
                output = output.replace('minestuck:', '')
            
            # Extract mode (and/or)
            mode = data.get('mode', '')
            
            if output and mode:
                if output not in alchemy_recipes:
                    alchemy_recipes[output] = {'modes': set()}
                alchemy_recipes[output]['modes'].add(mode)
        except Exception as e:
            print(f"Warning: Error parsing {json_file}: {e}")
    
    # Convert sets to lists for JSON serialization
    for item_id in alchemy_recipes:
        alchemy_recipes[item_id]['modes'] = sorted(list(alchemy_recipes[item_id]['modes']))
    
    return alchemy_recipes


def main():
    """Main function to parse items and generate JSON."""
    # Path to MSItems.java
    java_file = Path(__file__).parent.parent / 'src' / 'main' / 'java' / 'com' / 'mraof' / 'minestuck' / 'item' / 'MSItems.java'
    
    if not java_file.exists():
        print(f"Error: Could not find MSItems.java at {java_file}")
        return
    
    print(f"Parsing {java_file}...")
    items = parse_msitems_java(java_file)
    
    # Format names
    for item_key, item_data in items.items():
        item_data['name'] = format_item_name(item_key)
    
    print(f"Found {len(items)} items")
    
    # Parse grist costs
    grist_costs_dir = Path(__file__).parent.parent / 'src' / 'main' / 'generated' / 'resources' / 'data' / 'minestuck' / 'recipe' / 'grist_costs'
    print(f"\nParsing grist costs from {grist_costs_dir}...")
    grist_costs = parse_grist_costs(grist_costs_dir)
    print(f"Found grist costs for {len(grist_costs)} items")
    
    # Parse alchemy recipes
    combinations_dir = Path(__file__).parent.parent / 'src' / 'main' / 'generated' / 'resources' / 'data' / 'minestuck' / 'recipe' / 'combinations'
    print(f"\nParsing alchemy recipes from {combinations_dir}...")
    alchemy_recipes = parse_alchemy_recipes(combinations_dir)
    print(f"Found alchemy recipes for {len(alchemy_recipes)} items")
    
    # Add grist costs and alchemy info to items
    for item_key in items:
        if item_key in grist_costs:
            items[item_key]['grist_cost'] = grist_costs[item_key]
        
        if item_key in alchemy_recipes:
            items[item_key]['alchemy_modes'] = alchemy_recipes[item_key]['modes']
    
    # Save to JSON
    output_file = Path(__file__).parent / 'items_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, sort_keys=True)
    
    print(f"\nSaved item data to {output_file}")
    
    # Print some statistics
    types = {}
    for item_data in items.values():
        item_type = item_data.get('type', 'Unknown')
        types[item_type] = types.get(item_type, 0) + 1
    
    print("\nItem types:")
    for item_type, count in sorted(types.items()):
        print(f"  {item_type}: {count}")
    
    # Print grist and alchemy stats
    items_with_grist = sum(1 for item in items.values() if 'grist_cost' in item)
    items_with_alchemy = sum(1 for item in items.values() if 'alchemy_modes' in item)
    print(f"\nItems with grist costs: {items_with_grist}")
    print(f"Items with alchemy recipes: {items_with_alchemy}")


if __name__ == '__main__':
    main()
