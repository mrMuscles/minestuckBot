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

### `/item`
A simple command that replies with "Item Get!"

**Usage:** `/item`

**Response:** "Item Get!"

**Note:** This will be enhanced in the future with auto-updating parameters based on user input.

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

## Future Enhancements

- Tree commands with auto-updating parameters for `/item` and `/description`
- Integration with Minestuck mod data
- Additional commands for mod information and gameplay help
