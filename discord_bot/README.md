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

### `/description`
A simple command that replies with "Description Of Object!"

**Usage:** `/description`

**Response:** "Description Of Object!"

**Note:** This will be enhanced in the future with auto-updating parameters based on user input.

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

## Future Enhancements

- Integration with more Minestuck mod data
- Additional commands for mod information and gameplay help
- Recipe lookup
- Grist cost information
- Achievement/advancement tracking
