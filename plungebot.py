import discord
from discord.ext import commands, tasks
from itertools import cycle
import random
import json

# The prefix for all the commands
prefix = "p."
client = commands.Bot(command_prefix = prefix)
client.remove_command('help')

with open('auth.json', 'r') as f:
    data = json.load(f)

# Displays that the bot is ready
@client.event
async def on_ready():
    change_status.start()
    print('Bot is ready.')

# Gets the amount of drops
def getDrops():
    with open('info.json', 'r') as f:
        drops = json.load(f)
    
    return drops["drops"]

# Loops every 10 seconds and updates the game presence
@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(
        activity=discord.Game('Dropped ' + str(getDrops()) + " times!")
    )

# Creates the prefixes default value
# @client.event
# async def on_guild_join(guild):
#     with open('prefixes.json', 'r') as f:
#         prefixes = json.load(f)
    
#     prefixes[str(guild.id)] = '-'

#     with open('prefixes.json', 'w') as f:
#         json.dump(prefixes, f, indent=4)

# Removes the prefix for that server
# @client.event
# async def on_guild_remove(guild):
#     with open('prefixes.json', 'r') as f:
#         prefixes = json.load(f)
    
#     prefixes.pop(str(guild.id))

#     with open('prefixes.json', 'w') as f:
#         json.dump(prefixes, f, indent=4)

# Help Command
@client.command()
async def help(ctx):
    embed=discord.Embed(title="Plunge", description="List of Commands", color=0xfd5d5d)
    embed.add_field(name="General", value=f"`{prefix}drop`, `{prefix}help`, `{prefix}invite`", inline=False)
    await ctx.send(embed=embed)

# Command to let the user know where to drop using the drop command
@client.command()
async def drop(ctx):
    with open('info.json', 'r') as f:
        drops = json.load(f)
    
    drops["drops"] += 1

    with open('info.json', 'w') as f:
        json.dump(drops, f, indent=4)

    locations = ['Catty Corner', 'Frenzy Farm', 'Holly Hedges', 'Lazy Lake', 'Misty Meadows', 'Pleasant Park', 'Retail Row', 'Rickety Rig', 'Risky Reels', 'Salty Springs', 'Steamy Stacks', 'Sweaty Sands', 'The Authority', 'The Fortilla', 'The Grotto', 'The Shark']
    await ctx.send("You are dropping at: " + random.choice(locations))

# Command to invite the bot to your server
@client.command()
async def invite(ctx):
    embed=discord.Embed(title="Plunge Invite Link", description="If you'd like to invite this bot to your own server, [click here](https://discord.com/api/oauth2/authorize?client_id=732864657932681278&permissions=313408&scope=bot) for an invite", color=0xfd5d5d)
    await ctx.send(embed=embed)

@client.command()
async def botservers(ctx):
    await ctx.send("I'm in " + str(len(client.guilds)) + " servers")

client.run(data['token'])