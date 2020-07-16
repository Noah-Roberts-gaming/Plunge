import discord
from discord.ext import commands
import random
import json

# Gets the prefix from the json file
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

# The prefix for all the commands
client = commands.Bot(command_prefix = get_prefix)

with open('auth.json', 'r') as f:
    data = json.load(f)

# Displays that the bot is ready
@client.event
async def on_ready():
    print('Bot is ready.')

# Creates the prefixes default value
@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    
    prefixes[str(guild.id)] = '-'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

# Removes the prefix for that server
@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    
    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

# Command to change the prefix for the bot
@client.command()
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    
    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

# Command to let the user know where to drop using the drop command
@client.command()
async def drop(ctx):
    locations = ['Catty Corner', 'Frenzy Farm', 'Holly Hedges', 'Lazy Lake', 'Misty Meadows', 'Pleasant Park', 'Retail Row', 'Rickety Rig', 'Risky Reels', 'Salty Springs', 'Steamy Stacks', 'Sweaty Sands', 'The Authority', 'The Fortilla', 'The Grotto', 'The Shark']
    await ctx.send("You are dropping at: " + random.choice(locations))

client.run(data['token'])