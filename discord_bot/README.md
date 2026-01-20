# Minestuck Discord Bot

A Discord bot for the Minestuck community with command functionality.

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the bot token:**
   - Open `Token.env` in the root directory
   - Replace `YOUR_BOT_TOKEN_HERE` with your actual Discord bot token
   - You can get a bot token from the [Discord Developer Portal](https://discord.com/developers/applications)

3. **Run the bot:**
   ```bash
   python bot.py
   ```

## Commands

The bot currently supports the following slash commands:

### `/syncapp`
Syncs all app commands to Discord immediately. This command is useful when you add new commands or update existing ones.

**Usage:** `/syncapp`

**Response:** Confirmation message with the number of synced commands (ephemeral)

### `/item [item_name]`
Get detailed information about any item in the Minestuck game.

**Usage:** `/item <item_name>`

**Features:**
- **Autocomplete:** As you type, the bot shows the top 5 matching items sorted alphabetically
- **Forced Selection:** You must select an item from the autocomplete list
- **Detailed Information:** Shows item type, tier, rarity, attack stats, durability, special effects, and more

**Example:** `/item unbreakable_katana`

**Response:** 
- Initial: "Starting Slime's Enough Items Service..."
- Then displays a rich embed with all available item information including:
  - Item type (Weapon, Block, Armor, etc.)
  - Material/Tier
  - Rarity
  - Attack Damage & Speed (for weapons)
  - Durability
  - Efficiency (for tools)
  - Max Stack Size
  - Special Effects
  - Properties

### `/description [topic] [subtopic]`
Get detailed information about Minestuck game mechanics, systems, and features.

**Usage:** `/description <topic>` or `/description <topic> <subtopic>`

**Features:**
- **Autocomplete:** As you type the topic, the bot shows matching topics and subtopics
- **105+ Main Topics:** Covers grist types, alchemy, underlings, consorts, lands, gates, game mechanics, strife specibi, and much more
- **21+ Subtopics:** Deep dives into specific variants (e.g., individual grist types under the main "grist" topic)
- **Rich Descriptions:** Detailed explanations mixing English descriptions with technical/programming details
- **Images:** Each topic includes relevant imagery from the mod
- **Total Coverage:** 126+ total description entries (main topics + subtopics)

**Examples:** 
- `/description grist` - General information about the grist system
- `/description grist marble` - Specific information about marble grist
- `/description alchemy` - How the alchemy system works
- `/description underlings` - Information about enemy types
- `/description echeladder` - Progression system details

**Topics Include:**
- **Grist System:** Main grist concept + 20 grist types (build, amber, marble, diamond, zillium, etc.)
- **Alchemy:** Alchemy system, combinations, grist costs, machines (alchemiter, totem lathe, etc.)
- **Enemies:** Underlings, imps, ogres, basilisks, giclops, liches
- **NPCs:** Consorts, carapacians, denizens
- **World:** Lands, gates, entry, Medium, Prospit, Derse, Skaia
- **Game Mechanics:** Echeladder, god tiers, aspects, classes, quest beds, prototyping
- **Strife Specibi:** All weapon categories (hammerkind, bladekind, sicklekind, etc.)
- **Materials:** Tool/weapon materials (uranium, emerald, zilly, denizen, etc.)
- **Technical:** Programming details, APIs, world generation, entity systems

**Note:** Items, blocks, and armor are excluded as `/item` already covers those.

## Bot Permissions

The bot requires the following permissions:
- Send Messages
- Use Slash Commands
- Read Message History

## Maintaining the Items Database

The `/item` command reads item information from `items_data.json`, which is generated from the Minestuck mod's Java source code.

**To update the items database:**

1. Make sure you have the latest Minestuck source code in the repository
2. Run the item parser script:
   ```bash
   cd discord_bot
   python parse_items.py
   ```
3. This will regenerate `items_data.json` with the latest item information from `src/main/java/com/mraof/minestuck/item/MSItems.java`

**Note:** The items database should be regenerated whenever:
- New items are added to the mod
- Item properties are changed
- Item stats are rebalanced

## Maintaining the Descriptions Database

The `/description` command reads from `descriptions_data.json`, which contains detailed information about Minestuck game mechanics and systems.

**To update the descriptions database:**

1. The descriptions are primarily manually curated but can be enhanced with source code data
2. Run the descriptions parser script to update with technical details:
   ```bash
   cd discord_bot
   python parse_descriptions.py
   ```
3. This will update `descriptions_data.json` with technical information extracted from the source code (grist properties, entity types, etc.)

**Manual updates:**
- The main description content is hand-written for quality and clarity
- To add new topics, edit `descriptions_data.json` directly following the existing format
- Each topic should have: `name`, `description`, `image_url`, and optional `subtopics`

**Note:** The descriptions database should be updated whenever:
- New major game mechanics are added to the mod
- Existing systems are significantly changed
- You want to add more detail or correct information

## Future Enhancements

- Integration with more Minestuck mod data
- Additional commands for mod information and gameplay help
- Recipe lookup
- Grist cost information
- Achievement/advancement tracking
