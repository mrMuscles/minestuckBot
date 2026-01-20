# /item Command Usage Guide

The `/item` command allows you to look up detailed information about any item in the Minestuck mod.

## How to Use

1. Type `/item` in any Discord channel where the bot is present
2. Start typing an item name
3. Discord will show autocomplete suggestions (top 5 matches, sorted alphabetically)
4. Select an item from the list
5. Press Enter to send the command

## Examples

### Example 1: Looking up Unbreakable Katana
```
/item unb
```
As you type "unb", the autocomplete will show "Unbreakable Katana". Select it and press Enter.

**Response:**
```
Starting Slime's Enough Items Service...
```
Then displays an embed with:
- Name: Unbreakable Katana
- Type: Sword
- Material/Tier: Zilly
- Rarity: Rare
- Attack Damage: 6
- Attack Speed: -2.4
- Efficiency: 15.0
- Max Stack: 64
- Properties: Unbreakable, Sweeping attack

### Example 2: Searching for swords
```
/item sword
```
Autocomplete shows the first 5 swords alphabetically:
- Beef Sword
- Cinnamon Sword
- Emerald Sword
- Irradiated Steak Sword
- Music Sword

### Example 3: Looking up a specific item
```
/item claw_hammer
```
Shows details for the Claw Hammer:
- Type: Hammer
- Material/Tier: Iron
- Attack Damage: 2
- Attack Speed: -2.8
- Efficiency: 1.0
- Max Stack: 64

## Features

### Autocomplete
- Shows top 5 matching items as you type
- Sorted alphabetically for easy finding
- Searches both item names and IDs
- Updates dynamically as you type

### Information Displayed
The embed shows different information depending on the item type:

**For Weapons:**
- Attack Damage
- Attack Speed
- Efficiency
- Durability
- Special effects (fire, poison, sweeping, etc.)

**For Blocks:**
- Type
- Rarity
- Max Stack Size

**For All Items:**
- Name
- Type (Sword, Hammer, Axe, Block, etc.)
- Material/Tier (Iron, Diamond, Zilly, etc.)
- Rarity (Common, Uncommon, Rare, Epic)
- Max Stack Size
- Special Properties (Unbreakable, Fire Resistant, etc.)

## Tips

- Type just the first few letters to narrow down results quickly
- The search is case-insensitive
- You can search by the internal item ID (e.g., "unbreakable_katana")
- You must select from the autocomplete list - you cannot type a custom value

## Item Categories

The bot knows about 576 items across these categories:
- **Weapons:** Swords (34), Hammers (19), Axes (23), Knives (12), etc.
- **Tools:** Keys (24), Batons (6), Fans (10), etc.
- **Blocks:** Various decorative and functional blocks
- **Armor:** 20 different armor pieces
- **Items:** 322 miscellaneous items

## Troubleshooting

**Q: The item I want doesn't appear in autocomplete**
- Try different keywords (e.g., "unb" instead of "unbreakable")
- Check the spelling
- The item might be named differently than expected

**Q: I get "Item not found"**
- Make sure you selected from the autocomplete list
- Try searching again with different keywords

**Q: The bot doesn't respond**
- Make sure the bot is online
- Check that you have permission to use commands in the channel
- The bot may need to sync commands (contact a server admin)

## Keeping Data Updated

The item database is generated from the Minestuck mod's source code. When new items are added or existing items are updated:

1. The repository maintainer runs `python parse_items.py` in the `discord_bot` directory
2. This regenerates `items_data.json` with the latest item information
3. The bot is restarted to load the new data

Item data is current as of the last update to `items_data.json`.
