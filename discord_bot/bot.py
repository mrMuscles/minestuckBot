"""
Minestuck Discord Bot
A Discord bot for the Minestuck community with basic command functionality.
"""

import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from Token.env
# Token.env is in the root directory
root_dir = Path(__file__).parent.parent
load_dotenv(root_dir / 'Token.env')

# Get the Discord token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

# Define intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    print('------')

# Sync all app commands on bot startup
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")
    print('------')

# Command: /item - Replies with "Item Get!"
@bot.tree.command(name="item", description="Get an item")
async def item(interaction: discord.Interaction):
    """Replies with 'Item Get!'"""
    await interaction.response.send_message("Item Get!")

# Command: /description - Replies with "Description Of Object!"
@bot.tree.command(name="description", description="Get description of an object")
async def description(interaction: discord.Interaction):
    """Replies with 'Description Of Object!'"""
    await interaction.response.send_message("Description Of Object!")

# Run the bot
if __name__ == "__main__":
    if not TOKEN or TOKEN.strip() == "":
        print("Error: Please set your DISCORD_TOKEN in Token.env file")
        exit(1)

    bot.run(TOKEN)
