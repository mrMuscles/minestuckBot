"""
Minestuck Discord Bot
A Discord bot for the Minestuck community with basic command functionality.
"""

import discord
from discord import app_commands
from discord.ext import commands
import os
import json
from dotenv import load_dotenv
from pathlib import Path
from typing import List

# Load environment variables from Token.env
# Token.env is in the root directory
root_dir = Path(__file__).parent.parent
load_dotenv(root_dir / 'Token.env')

# Get the Discord token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

# Define intents
intents = discord.Intents.default()
intents.message_content = True

# Default max stack size in Minecraft
DEFAULT_STACK_SIZE = 64

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Load items data
ITEMS_DATA = {}
items_file = Path(__file__).parent / 'items_data.json'
if items_file.exists():
    with open(items_file, 'r', encoding='utf-8') as f:
        ITEMS_DATA = json.load(f)
    print(f"Loaded {len(ITEMS_DATA)} items from items_data.json")
else:
    print(f"Warning: items_data.json not found at {items_file}")
    print("Run parse_items.py to generate the items database")

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

# Autocomplete function for item names
async def item_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    """
    Autocomplete function for item names.
    Returns top 5 items that match the current input, sorted lexicographically.
    """
    current_lower = current.lower()
    
    # Filter items that match the input
    matching_items = []
    for item_id, item_data in ITEMS_DATA.items():
        item_name = item_data.get('name', item_id)
        if current_lower in item_name.lower() or current_lower in item_id.lower():
            matching_items.append((item_name, item_id))
    
    # Sort lexicographically by name
    matching_items.sort(key=lambda x: x[0].lower())
    
    # Return top 5 matches
    return [
        app_commands.Choice(name=name, value=item_id)
        for name, item_id in matching_items[:5]
    ]


# Command: /item - Get information about a Minestuck item
@bot.tree.command(name="item", description="Get information about any item in the Minestuck game")
@app_commands.autocomplete(item=item_autocomplete)
async def item(interaction: discord.Interaction, item: str):
    """
    Display detailed information about a Minestuck item.
    
    Parameters:
    -----------
    item: str
        The item to look up (autocomplete enabled)
    """
    # Send initial "loading" message
    await interaction.response.send_message("Starting Slime's Enough Items Service...")
    
    # Check if item exists
    if item not in ITEMS_DATA:
        await interaction.edit_original_response(content=f"❌ Item '{item}' not found in the database.")
        return
    
    item_data = ITEMS_DATA[item]
    item_name = item_data.get('name', item.replace('_', ' ').title())
    
    # Create embed
    embed = discord.Embed(
        title=f"📦 {item_name}",
        description=f"Information about **{item_name}**",
        color=discord.Color.blue()
    )
    
    # Add item type
    item_type = item_data.get('type', 'Unknown')
    embed.add_field(name="Type", value=item_type, inline=True)
    
    # Add tier if available
    tier = item_data.get('tier')
    if tier:
        embed.add_field(name="Material/Tier", value=tier, inline=True)
    
    # Add rarity if in attributes
    attributes = item_data.get('attributes', [])
    rarity_attrs = [attr for attr in attributes if 'Rarity' in attr]
    if rarity_attrs:
        rarity = rarity_attrs[0].replace('Rarity: ', '')
        embed.add_field(name="Rarity", value=rarity, inline=True)
    else:
        embed.add_field(name="Rarity", value="Common", inline=True)
    
    # Combat stats (for weapons)
    attack_damage = item_data.get('attack_damage')
    attack_speed = item_data.get('attack_speed')
    if attack_damage is not None and attack_damage >= 0:
        embed.add_field(name="⚔️ Attack Damage", value=f"{attack_damage}", inline=True)
    if attack_speed is not None:
        embed.add_field(name="⚡ Attack Speed", value=f"{attack_speed}", inline=True)
    
    # Durability
    durability = item_data.get('durability')
    if durability:
        embed.add_field(name="🛡️ Durability", value=f"{durability}", inline=True)
    
    # Efficiency (for tools)
    efficiency = item_data.get('efficiency')
    if efficiency and efficiency > 0:
        embed.add_field(name="⛏️ Efficiency", value=f"{efficiency}", inline=True)
    
    # Max stack size
    stack_attrs = [attr for attr in attributes if 'Max Stack' in attr]
    if stack_attrs:
        embed.add_field(name="📚 Max Stack", value=stack_attrs[0].replace('Max Stack: ', ''), inline=True)
    else:
        embed.add_field(name="📚 Max Stack", value=str(DEFAULT_STACK_SIZE), inline=True)
    
    # Special attributes
    special_attrs = [attr for attr in attributes if 'Rarity' not in attr and 'Max Stack' not in attr]
    if special_attrs:
        # Group into categories
        effects = []
        properties = []
        
        for attr in special_attrs:
            if any(keyword in attr.lower() for keyword in ['effect', 'damage', 'fire', 'poison', 'wither', 'attack', 'backstab']):
                effects.append(attr)
            else:
                properties.append(attr)
        
        if effects:
            embed.add_field(name="✨ Special Effects", value='\n'.join(f"• {effect}" for effect in effects), inline=False)
        
        if properties:
            embed.add_field(name="🔧 Properties", value='\n'.join(f"• {prop}" for prop in properties), inline=False)
    
    # Item ID (for reference)
    embed.set_footer(text=f"Item ID: {item}")
    
    # Update the message with the embed
    await interaction.edit_original_response(content=None, embed=embed)

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
