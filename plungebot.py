import discord
from discord.ext import commands, tasks
import random
import json

# The prefix for all the commands
prefix = "p."
client = commands.Bot(command_prefix = prefix, case_insensitive=True)
client.remove_command('help')

# Reads the Auth.json File
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

def isDev(id):
    if id == 260698008595726336 or id == 534099020230950923 or id == 290530439331053579:
        return True 
    else:
        return False

# TODO: Cycle through the presences Servers, Drops, P.help, Funny message???
# Loops every 10 seconds and updates the game presence ("Playing Dropped 84 Times")
@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(
        activity=discord.Game('Dropped ' + str(getDrops()) + " times!")
    )

# Command Not Found Error Handler
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url="https://i.imgur.com/tdbgl13.png")
        embed.add_field(name="Command Not Found", value="Try `p.help` for a list of all commands.", inline=False)
        await ctx.send(embed=embed)


# Help Command
# p.help
@client.command()
async def help(ctx, setting = None):
    if setting is None:
        embed=discord.Embed(title="Plunge", description="List of Commands", color=0xfd5d5d)
        embed.set_thumbnail(url="https://i.imgur.com/tdbgl13.png")
        embed.add_field(name="General", value=f"`{prefix}drop`, `{prefix}help`, `{prefix}suggest`, `{prefix}invite`, `{prefix}discord`", inline=False)
        embed.set_footer(text="p.invite • Invites this bot to your server")
        await ctx.send(embed=embed)
    elif setting.lower() == "drop":
        # Code
        return
    elif setting.lower() == "suggest":
        # Code
        return
    elif setting.lower() == "invite":
        # Code
        return
    elif setting.lower() == "discord" or setting.lower() == "server" or setting.lower() == "join":
        # Code
        return
    else:
        # Invalid Setting
        return
        

# Command to let the user know where to drop using the drop command
# p.drop
@client.command()
async def drop(ctx):
    with open('info.json', 'r') as f:
        drops = json.load(f)
    
    drops["drops"] += 1

    with open('info.json', 'w') as f:
        json.dump(drops, f, indent=4)

    # Removed: "The Shark"
    locations = ['Catty Corner', 'Frenzy Farm', 'Holly Hedges', 'Lazy Lake', 'Misty Meadows', 'Pleasant Park', 'Retail Row', 'Rickety Rig', 'Salty Springs', 'Steamy Stacks', 'Sweaty Sands', 'The Authority', 'The Fortilla', 'Risky Reels', 'The Yacht', 'Dirty Docks', 'Broken Castle', 'Pirate Barge']
    location = random.choice(locations)

    locationurl = ''

    # Based on the location, set the image url
    if location == 'Catty Corner':
        locationurl = 'https://i.imgur.com/IN3zcJJ.png'
    elif location == 'Frenzy Farm':
        locationurl = 'https://i.imgur.com/c1pYdgs.png'
    elif location == 'Holly Hedges':
        locationurl = 'https://i.imgur.com/GX2A97E.png'
    elif location == 'Lazy Lake':
        locationurl = 'https://i.imgur.com/cNlKs5b.png'
    elif location == 'Misty Meadows':
        locationurl = 'https://i.imgur.com/QneWdkB.png'
    elif location == 'Pleasant Park':
        locationurl = 'https://i.imgur.com/cuIXiTM.png'
    elif location == 'Retail Row':
        locationurl = 'https://i.imgur.com/sIuNMV4.png'
    elif location == 'Rickety Rig':
        locationurl = 'https://i.imgur.com/tsJPpyn.png'
    elif location == 'Salty Springs':
        locationurl = 'https://i.imgur.com/KBFUFPN.png'
    elif location == 'Steamy Stacks':
        locationurl = 'https://i.imgur.com/QLPw5Bb.png'
    elif location == 'Sweaty Sands':
        locationurl = 'https://i.imgur.com/9eQBa08.png'
    elif location == 'The Authority':
        locationurl = 'https://i.imgur.com/JXWhuzJ.png'
    elif location == 'The Fortilla':
        locationurl = 'https://i.imgur.com/EOeio4u.png'
    elif location == 'Risky Reels':
        locationurl = 'https://i.imgur.com/K6Zwis8.png'
    elif location == 'The Yacht':
        locationurl = 'https://i.imgur.com/OLyro4T.png'
    elif location == 'Dirty Docks':
        locationurl = 'https://i.imgur.com/sPrr5rY.png'
    elif location == 'Broken Castle':
        locationurl = 'https://i.imgur.com/DocMZvk.png'
    elif location == 'Pirate Barge':
        locationurl = 'https://i.imgur.com/qpcf2bd.png'
    else:
        # Hmm thats odd
        locationurl = ''

    embed=discord.Embed(title="Plunge", color=0xfd5d5d)
    embed.add_field(name="You are dropping at:", value=location, inline=False)
    embed.set_thumbnail(url="https://i.imgur.com/tdbgl13.png")
    embed.set_image(url=locationurl)
    embed.set_footer(text="p.invite • Invites this bot to your server")
    await ctx.send(embed=embed)

# Command to invite the bot to your server
# p.invite
@client.command()
async def invite(ctx):
    embed=discord.Embed(title="Plunge Invite Link", description="If you'd like to invite this bot to your own server, [click here](https://discord.com/api/oauth2/authorize?client_id=732864657932681278&permissions=313408&scope=bot) for an invite", color=0xfd5d5d)
    embed.set_thumbnail(url="https://i.imgur.com/tdbgl13.png")
    await ctx.send(embed=embed)

# Command to see how many servers the bot is in
# p.servers, p.botservers, p.botserver
@client.command(aliases=['botservers', 'botserver'])
async def servers(ctx):
    if isDev(ctx.author.id):
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url="https://i.imgur.com/tdbgl13.png")
        embed.add_field(name="Plunge is in:", value=f"{str(len(client.guilds))} servers", inline=False)
        await ctx.send(embed=embed)
    else:
        return

# Command to join the developer discord
# p.server, p.join, p.discord
@client.command(aliases=['join', 'discord'])
async def server(ctx):
    embed=discord.Embed(title="Plunge Development", description="To join our discord, [click here](https://discord.gg/mjr6nUU) for an invite", color=0xfd5d5d)
    embed.set_thumbnail(url="https://i.imgur.com/tdbgl13.png")
    embed.set_footer(text="p.invite • Invites this bot to your server")
    await ctx.send(embed=embed)
    
@client.command()
async def suggest(ctx, *, suggestion = None):
    if suggestion is None:
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url="https://i.imgur.com/tdbgl13.png")
        embed.add_field(name="Invalid Command Format", value="Try: `p.suggest (suggestion)`", inline=False)
        await ctx.send(embed=embed)
    else:
        # On Suggestion command, ping private discord channel 733592146308890675 with the details
        channelId = client.get_channel(733592146308890675) #suggestions in Plunge Development

        # Response to user's message
        reply=discord.Embed(title="Plunge", color=0xfd5d5d)
        reply.set_thumbnail(url="https://i.imgur.com/tdbgl13.png")
        reply.add_field(name="Suggestion Sent", value="Thanks for submitting your suggestion!", inline=False)
        reply.set_footer(text="p.invite • Invites this bot to your server")
        await ctx.send(embed=reply)
        
        # Suggestion added to suggestions channel
        suggested=discord.Embed(title="Plunge", description=f"Submitted by {ctx.author.name}#{ctx.author.discriminator}", color=0xfd5d5d)
        suggested.set_thumbnail(url=ctx.author.avatar_url)
        suggested.add_field(name="Suggestion", value=suggestion, inline=False)
        await channelId.send(embed=suggested)

# Runs the bot
client.run(data['token'])