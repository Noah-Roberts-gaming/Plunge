import discord
from discord.ext import commands
import random
import json

# The prefix for all the commands
client = commands.Bot(command_prefix = '-')

with open('auth.json') as f:
    data = json.load(f)

# Displays that the bot is ready
@client.event
async def on_ready():
    print('Bot is ready.')

# Lets the user know where to drop using -drop
@client.command()
async def drop(ctx):
    locations = ['Catty Corner', 'Frenzy Farm', 'Holly Hedges', 'Lazy Lake', 'Misty Meadows', 'Pleasant Park', 'Retail Row', 'Rickety Rig', 'Risky Reels', 'Salty Springs', 'Steamy Stacks', 'Sweaty Sands', 'The Authority', 'The Fortilla', 'The Grotto', 'The Shark']
    await ctx.send("You are dropping at: " + random.choice(locations))

client.run(data['token'])