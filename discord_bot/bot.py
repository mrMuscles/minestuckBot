"""
Minestuck Discord Bot
A Discord bot for the Minestuck community with basic command functionality.
"""

import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from Token.env
# Token.env is in the root directory
import sys
from pathlib import Path
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

# Command: /syncapp - Syncs all app commands to Discord
@bot.tree.command(name="syncapp", description="Sync all app commands to Discord immediately")
async def syncapp(interaction: discord.Interaction):
    """Syncs all app commands to Discord"""
    await interaction.response.defer(ephemeral=True)
    try:
        synced = await bot.tree.sync()
        await interaction.followup.send(f"Synced {len(synced)} commands successfully!", ephemeral=True)
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        await interaction.followup.send(f"Failed to sync commands: {e}", ephemeral=True)
        print(f"Error syncing commands: {e}")

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
    if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("Error: Please set your DISCORD_TOKEN in Token.env file")
        exit(1)
    
    bot.run(TOKEN)
