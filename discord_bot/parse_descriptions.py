#!/usr/bin/env python3
"""
Parse Minestuck source code to generate or update description data.
This script can be run to regenerate descriptions_data.json from the source code.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any


def parse_grist_types(grist_types_file: Path) -> Dict[str, Dict[str, Any]]:
    """Parse GristTypes.java to extract grist type information."""
    grist_descriptions = {}
    
    if not grist_types_file.exists():
        print(f"Warning: GristTypes.java not found at {grist_types_file}")
        return grist_descriptions
    
    with open(grist_types_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match grist type registrations
    # Example: public static final Supplier<GristType> BUILD = GRIST_TYPES.register("build", () -> new GristType(new GristType.Properties(1.0F, 1).candy(MSItems.BUILD_GUSHERS)));
    pattern = r'public static final Supplier<GristType>\s+(\w+)\s*=\s*GRIST_TYPES\.register\("([^"]+)",\s*\(\)\s*->\s*new GristType\(new GristType\.Properties\(([^,]+),\s*([^)]+)\)([^;]+)\)\);'
    
    matches = re.findall(pattern, content)
    
    for match in matches:
        const_name, grist_id, spawn_weight, power = match[0], match[1], match[2], match[3]
        additional_props = match[4]
        
        # Extract candy item
        candy_match = re.search(r'\.candy\(MSItems\.([^)]+)\)', additional_props)
        candy_item = candy_match.group(1) if candy_match else None
        
        # Extract underling color
        color_match = re.search(r'\.underlingType\(0x([0-9a-fA-F]+)\)', additional_props)
        underling_color = f"0x{color_match.group(1)}" if color_match else None
        
        grist_descriptions[grist_id] = {
            'const_name': const_name,
            'spawn_weight': spawn_weight.replace('F', ''),
            'power': power,
            'candy': candy_item,
            'color': underling_color
        }
    
    print(f"Found {len(grist_descriptions)} grist types in source code")
    return grist_descriptions


def parse_entity_types(entity_dir: Path) -> List[str]:
    """Parse entity directory to find underling types."""
    if not entity_dir.exists():
        return []
    
    entities = []
    underling_dir = entity_dir / 'underling'
    if underling_dir.exists():
        for java_file in underling_dir.glob('*Entity.java'):
            entity_name = java_file.stem.replace('Entity', '').lower()
            if entity_name not in ['underling', 'underlingsettings']:
                entities.append(entity_name)
    
    print(f"Found {len(entities)} underling types")
    return entities


def update_descriptions_with_source_data():
    """Update descriptions_data.json with data parsed from source code."""
    # Paths to source files
    base_dir = Path(__file__).parent.parent
    grist_types_file = base_dir / 'src' / 'main' / 'java' / 'com' / 'mraof' / 'minestuck' / 'api' / 'alchemy' / 'GristTypes.java'
    entity_dir = base_dir / 'src' / 'main' / 'java' / 'com' / 'mraof' / 'minestuck' / 'entity'
    
    # Load existing descriptions
    descriptions_file = Path(__file__).parent / 'descriptions_data.json'
    with open(descriptions_file, 'r', encoding='utf-8') as f:
        descriptions = json.load(f)
    
    # Parse grist types
    grist_data = parse_grist_types(grist_types_file)
    
    # Update grist subtopics with source data
    if 'grist' in descriptions and grist_data:
        grist_topic = descriptions['grist']
        subtopics = grist_topic.get('subtopics', {})
        
        for grist_id, data in grist_data.items():
            if grist_id in subtopics:
                # Add technical details to existing description
                existing_desc = subtopics[grist_id].get('description', '')
                tech_note = f"\n\nTechnical: Spawn Weight: {data['spawn_weight']}, Power: {data['power']}"
                if data['candy']:
                    tech_note += f", Candy: {data['candy']}"
                if data['color']:
                    tech_note += f", Color: {data['color']}"
                
                # Only add if not already there
                if "Technical:" not in existing_desc:
                    subtopics[grist_id]['description'] = existing_desc + tech_note
    
    # Parse and update entity types
    underling_types = parse_entity_types(entity_dir)
    if underling_types:
        print(f"Underling types found: {', '.join(underling_types)}")
    
    # Save updated descriptions
    with open(descriptions_file, 'w', encoding='utf-8') as f:
        json.dump(descriptions, f, indent=2)
    
    print(f"\nUpdated descriptions_data.json with source code data")
    print(f"Total topics: {len(descriptions)}")


def main():
    """Main function."""
    print("Minestuck Descriptions Parser")
    print("=" * 50)
    print()
    print("This script updates descriptions_data.json with data from source code.")
    print("The base descriptions are manually curated, but this adds technical details.")
    print()
    
    try:
        update_descriptions_with_source_data()
        print("\n✓ Successfully updated descriptions database")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
