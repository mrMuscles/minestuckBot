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

# Base URL for item images (can be overridden via environment variable)
ITEM_IMAGE_BASE_URL = os.getenv('ITEM_IMAGE_BASE_URL', 'https://raw.githubusercontent.com/mrMuscles/minestuckBot/main/src/main/resources/assets/minestuck/textures/item')

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

# Load descriptions data
DESCRIPTIONS_DATA = {}
descriptions_file = Path(__file__).parent / 'descriptions_data.json'
if descriptions_file.exists():
    with open(descriptions_file, 'r', encoding='utf-8') as f:
        DESCRIPTIONS_DATA = json.load(f)
    print(f"Loaded {len(DESCRIPTIONS_DATA)} description topics from descriptions_data.json")
else:
    print(f"Warning: descriptions_data.json not found at {descriptions_file}")
    print("Run parse_descriptions.py to generate the descriptions database")

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    print('------')
    await bot.change_presence(activity=discord.Game(name="Minestuck Encyclopedia Service"))

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

    # Add item image as thumbnail
    # Images are stored in the GitHub repository
    # Can be overridden with ITEM_IMAGE_BASE_URL environment variable
    image_url = f"{ITEM_IMAGE_BASE_URL}/{item}.png"
    embed.set_thumbnail(url=image_url)

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

    # Grist costs
    grist_cost = item_data.get('grist_cost')
    if grist_cost:
        grist_text = ', '.join(f"{amount} {grist_type}" for grist_type, amount in grist_cost.items())
        embed.add_field(name="💎 Grist Cost", value=grist_text, inline=False)

    # Alchemy modes
    alchemy_modes = item_data.get('alchemy_modes')
    if alchemy_modes:
        # Format the modes
        if len(alchemy_modes) == 2:
            alchemy_text = "Both && and ||"
        elif len(alchemy_modes) == 1:
            mode = alchemy_modes[0]
            if mode == 'and':
                alchemy_text = "&&"
            elif mode == 'or':
                alchemy_text = "||"
            else:
                alchemy_text = mode
        else:
            alchemy_text = ', '.join(alchemy_modes)
        embed.add_field(name="⚗️ Alchemy Type", value=alchemy_text, inline=False)
    elif not grist_cost:
        # No grist cost and no alchemy - indicate this
        embed.add_field(name="⚗️ Alchemy", value="No alchemy recipe or grist cost", inline=False)

    # Item ID (for reference)
    embed.set_footer(text=f"Item ID: {item}")

    # Update the message with the embed
    await interaction.edit_original_response(content=None, embed=embed)

# Autocomplete function for description topics
async def topic_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    """
    Autocomplete function for description topics.
    Returns top 25 topics that match the current input, sorted lexicographically.
    """
    current_lower = current.lower()
    
    # Filter topics that match the input (both main topics and subtopics)
    matching_topics = []
    for topic_id, topic_data in DESCRIPTIONS_DATA.items():
        topic_name = topic_data.get('name', topic_id)
        if current_lower in topic_name.lower() or current_lower in topic_id.lower():
            matching_topics.append((topic_name, topic_id))
        
        # Also check subtopics
        subtopics = topic_data.get('subtopics', {})
        for subtopic_id, subtopic_data in subtopics.items():
            subtopic_name = subtopic_data.get('name', subtopic_id)
            full_name = f"{topic_name} - {subtopic_name}"
            full_id = f"{topic_id}:{subtopic_id}"
            if current_lower in subtopic_name.lower() or current_lower in subtopic_id.lower():
                matching_topics.append((full_name, full_id))
    
    # Sort lexicographically by name
    matching_topics.sort(key=lambda x: x[0].lower())
    
    # Return top 25 matches
    return [
        app_commands.Choice(name=name[:100], value=topic_id)  # Discord limits choice names to 100 chars
        for name, topic_id in matching_topics[:25]
    ]


# Autocomplete function for subtopics
async def subtopic_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    """
    Autocomplete function for subtopics based on the selected topic.
    """
    # Get the currently selected topic from the command
    topic = interaction.namespace.topic
    if not topic or ':' in topic:
        return []
    
    # Get subtopics for the selected topic
    topic_data = DESCRIPTIONS_DATA.get(topic, {})
    subtopics = topic_data.get('subtopics', {})
    
    if not subtopics:
        return []
    
    current_lower = current.lower()
    
    # Filter subtopics that match
    matching = []
    for subtopic_id, subtopic_data in subtopics.items():
        subtopic_name = subtopic_data.get('name', subtopic_id)
        if current_lower in subtopic_name.lower() or current_lower in subtopic_id.lower():
            matching.append((subtopic_name, subtopic_id))
    
    # Sort and return
    matching.sort(key=lambda x: x[0].lower())
    return [
        app_commands.Choice(name=name, value=subtopic_id)
        for name, subtopic_id in matching[:25]
    ]


# Command: /description - Get detailed descriptions about Minestuck mechanics
@bot.tree.command(name="description", description="Get detailed information about Minestuck game mechanics and systems")
@app_commands.autocomplete(topic=topic_autocomplete, subtopic=subtopic_autocomplete)
async def description(interaction: discord.Interaction, topic: str, subtopic: str = None):
    """
    Display detailed description about a Minestuck topic.
    
    Parameters:
    -----------
    topic: str
        The main topic to describe (autocomplete enabled)
    subtopic: str, optional
        Specific subtopic for more detailed information (autocomplete enabled)
    """
    # Send initial "loading" message
    await interaction.response.send_message("📚 Loading Minestuck Encyclopedia...")
    
    # Handle topic:subtopic format from autocomplete
    if ':' in topic:
        parts = topic.split(':', 1)
        topic = parts[0]
        subtopic = parts[1]
    
    # Check if topic exists
    if topic not in DESCRIPTIONS_DATA:
        await interaction.edit_original_response(content=f"❌ Topic '{topic}' not found in the database.")
        return
    
    topic_data = DESCRIPTIONS_DATA[topic]
    
    # If subtopic is specified, show subtopic instead
    if subtopic:
        subtopics = topic_data.get('subtopics', {})
        if subtopic not in subtopics:
            await interaction.edit_original_response(content=f"❌ Subtopic '{subtopic}' not found under '{topic}'.")
            return
        
        subtopic_data = subtopics[subtopic]
        display_name = subtopic_data.get('name', subtopic.replace('_', ' ').title())
        description_text = subtopic_data.get('description', 'No description available.')
        image_url = subtopic_data.get('image_url', '')
        
        # Create embed for subtopic
        embed = discord.Embed(
            title=f"📖 {display_name}",
            description=description_text,
            color=discord.Color.purple()
        )
        
        if image_url:
            embed.set_thumbnail(url=image_url)
        
        embed.set_footer(text=f"Topic: {topic} → {subtopic}")
    else:
        # Show main topic
        display_name = topic_data.get('name', topic.replace('_', ' ').title())
        description_text = topic_data.get('description', 'No description available.')
        image_url = topic_data.get('image_url', '')
        
        # Create embed for main topic
        embed = discord.Embed(
            title=f"📖 {display_name}",
            description=description_text,
            color=discord.Color.blue()
        )
        
        if image_url:
            embed.set_thumbnail(url=image_url)
        
        # Add subtopics field if they exist
        subtopics = topic_data.get('subtopics', {})
        if subtopics:
            subtopic_list = ', '.join([data.get('name', sid) for sid, data in list(subtopics.items())[:10]])
            if len(subtopics) > 10:
                subtopic_list += f"... and {len(subtopics) - 10} more"
            embed.add_field(
                name="📑 Related Subtopics",
                value=subtopic_list,
                inline=False
            )
        
        embed.set_footer(text=f"Topic ID: {topic}")
    
    # Update the message with the embed
    await interaction.edit_original_response(content=None, embed=embed)

# Run the bot
if __name__ == "__main__":
    if not TOKEN or TOKEN.strip() == "":
        print("Error: Please set your DISCORD_TOKEN in Token.env file")
        exit(1)

    bot.run(TOKEN)
