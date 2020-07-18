import discord
from discord.ext import commands, tasks
import random
import json
import asyncio

# The prefix for all the commands
prefix = "p."
client = commands.Bot(command_prefix = prefix, case_insensitive=True)
client.remove_command('help')

# The url for our logo
logourl = "https://i.imgur.com/tdbgl13.png"

# Reads the Auth.json File
with open('auth.json', 'r') as f:
    data = json.load(f)

# Loops every 10 seconds and updates the game presence ("Playing Dropped 84 Times")
#@tasks.loop(seconds=10)
async def change_status():
    while True:
        await client.change_presence(
            activity=discord.Game('Dropped ' + str(getDrops()) + " times!")
        )

        await asyncio.sleep(15)

        guilds = str(len([g for g in client.guilds]))  # Gets length of all client's guilds
        
        users = 0
        for guild in client.guilds:
            users += len(guild.members)        # Gets how many users are in all of the guilds combined

        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=f"s: {guilds} • u: {users}")
        )

        await asyncio.sleep(15)

        await client.change_presence(
            activity=discord.Game(' p.help • p.drop • p.invite')
        )

        await asyncio.sleep(15)

# Displays that the bot is ready
@client.event
async def on_ready():
    #change_status.start()
    client.loop.create_task(change_status())
    print('Bot is ready.')

# Gets the amount of drops
def getDrops():
    with open('info.json', 'r') as f:
        drops = json.load(f)
    
    return drops["drops"]

def isDev(ctx):
    if ctx.author.id == 260698008595726336 or ctx.author.id == 534099020230950923 or ctx.author.id == 290530439331053579:
        return True 
    else:
        return False

# Command Not Found Error Handler
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Command Not Found", value="Try `p.help` for a list of all commands.", inline=False)
        await ctx.send(embed=embed)

# When the bot is directly mentioned "@Plunge", give a description about what the bot is about
@client.event
async def on_message(message):
    if message.content == '<@!732864657932681278>':
        embed=discord.Embed(title="Plunge", description=f"Hey {message.author.mention}, can't decide on where to drop in Fortnite? It happens to us all, we  are riding in the battle bus with our maps open but no location marked.  Before we know it, we are getting kicked off the bus with little to no options to land. Luckily, Plunge Bot can help. With a simple command `p.drop`, Plunge will randomly select a location for you to drop in Fortnite, making your next drop stress free.", color=0xfd5d5d)
        embed.add_field(name="Info", value="Use `p.help` to get started", inline=False)
        embed.set_thumbnail(url=logourl)
        embed.set_footer(text="Created by The Plunge Team")
        await message.channel.send(embed=embed)
    await client.process_commands(message)

# Help Command
# p.help
@client.command()
async def help(ctx, setting = None):
    if setting is None:
        embed=discord.Embed(title="Plunge", description="List of Commands", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="General", value=f"`{prefix}drop`, `{prefix}help`, `{prefix}feedback`, `{prefix}invite`, `{prefix}discord`", inline=False)
        embed.add_field(name="Info", value=f"To get more help on a command or see the command's function, try: `p.help (command)`", inline=False)
        embed.set_footer(text="p.invite • Invites this bot to your server")
        await ctx.send(embed=embed)
    elif setting.lower() == "drop":
        embed=discord.Embed(title="Plunge", description="Drop Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Gives you a random location to drop in Fortnite!", inline=False)
        embed.add_field(name="Usage:", value="`p.drop`", inline=False)
        embed.set_footer(text="p.invite • Invites this bot to your server")
        await ctx.send(embed=embed)
    elif setting.lower() == "suggest" or setting.lower() == "feedback":
        embed=discord.Embed(title="Plunge", description="Feedback Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Sends feedback to the developers to review. -- Can also be used to submit suggestions.", inline=False)
        embed.add_field(name="Usage:", value="`p.feedback (feedback)`", inline=False)
        embed.add_field(name="Aliases:", value="`p.feedback`, `p.suggest`", inline=False)
        embed.set_footer(text="p.invite • Invites this bot to your server")
        await ctx.send(embed=embed)
    elif setting.lower() == "feedback":
        embed=discord.Embed(title="Plunge", description="Feedback Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Adds feedback for the developers to review.", inline=False)
        embed.add_field(name="Usage:", value="`p.feedback (your feedback)`", inline=False)
        embed.set_footer(text="p.invite • Invites this bot to your server")
        await ctx.send(embed=embed)
    elif setting.lower() == "invite":
        embed=discord.Embed(title="Plunge", description="Invite Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Gives you a link to invite this bot to your server!", inline=False)
        embed.add_field(name="Usage:", value="`p.invite`", inline=False)
        await ctx.send(embed=embed)
    elif setting.lower() == "discord" or setting.lower() == "server" or setting.lower() == "join" or setting.lower() == "support":
        embed=discord.Embed(title="Plunge", description="Discord Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Invites you to the bot's development server!", inline=False)
        embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
        embed.add_field(name="Aliases:", value="`p.discord`, `p.server`, `p.join`, `p.support`", inline=False)
        embed.set_footer(text="p.invite • Invites this bot to your server")
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Plunge", description="Invalid Command Setting", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Try:", value=f"`p.help` or `p.help (command)`", inline=False)
        await ctx.send(embed=embed)
        
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
    embed.set_thumbnail(url=logourl)
    embed.set_image(url=locationurl)
    embed.set_footer(text="p.invite • Invites this bot to your server")
    await ctx.send(embed=embed)

# Command to invite the bot to your server
# p.invite
@client.command()
async def invite(ctx):
    embed=discord.Embed(title="Plunge Invite Link", description="If you'd like to invite this bot to your own server, [click here](https://discord.com/api/oauth2/authorize?client_id=732864657932681278&permissions=313408&scope=bot) for an invite", color=0xfd5d5d)
    embed.set_thumbnail(url=logourl)
    await ctx.send(embed=embed)

# Command to see how many servers the bot is in
# p.servers, p.botservers, p.botserver
@client.command(aliases=['botservers', 'botserver'])
@commands.check(isDev)
async def servers(ctx):
    embed=discord.Embed(title="Plunge", color=0xfd5d5d)
    embed.set_thumbnail(url=logourl)
    embed.add_field(name="Plunge is in:", value=f"{str(len(client.guilds))} servers", inline=False)
    await ctx.send(embed=embed)

# Command to verify they added the bot to the server
# p.verify
# TODO: remove @commands.has_permissions(manage_guild=True) and manually check if the ctx.author has the manage_guild permission..
# if they do, do the following code.... else give them a message saying, you must have this bot in your own server to get promoted to a user role
@client.command()
@commands.has_permissions(manage_guild=True)
async def verify(ctx):
    ourGuild = client.get_guild(733551377611096195)

    users = []

    for user in ourGuild.members:
        users.append(user.id)

    if (ctx.author.id in users):
        await ourGuild.get_member(ctx.author.id).add_roles(ourGuild.get_role(733559654210207885), reason="Used the verify command")
        await ourGuild.get_member(ctx.author.id).remove_roles(ourGuild.get_role(733558248401272832), reason="Used the verify command")
        # TODO: Make the promoted to user message pretty
        # TODO: Save the ctx.guild.id and tie it to the ctx.author.id.... Store this in json formatted like this https://discordapp.com/channels/733551377611096195/733552092110913648/733997899742052404
        await ctx.send('Youre in')



# TODO: Make a command to remove users from the USER ROLE IN OUR GUILD if the bot is no longer in the guild
# 1: guildIDs = Grab the current guilds that the bot is in and store it in a variable

# 2: guildkeys = Grab all the Guild ID keys from the JSON REFERENCE?? --> https://stackoverflow.com/questions/15789059/python-json-only-get-keys-in-first-level
# open and read the json and save the keys from that  in its own list

# 3: for k in guildkeys
    # 4: if k not in guildIDS
        # 5: Remove the server from the json file including the user

# 6: userids = get all the userid's in the user role from our server

# 7: usersjson = get all the userId's from the already opened json above??? and store them in their own list variable

# 8: for user in userids
    # 9: if user not in usersjson
        #10: remove their role from the server


# Command to join the developer discord
# p.server, p.join, p.discord
@client.command(aliases=['join', 'discord'])
async def server(ctx):
    embed=discord.Embed(title="Plunge Development", description="To join our discord, [click here](https://discord.gg/mjr6nUU) for an invite", color=0xfd5d5d)
    embed.set_thumbnail(url=logourl)
    embed.set_footer(text="p.invite • Invites this bot to your server")
    await ctx.send(embed=embed)

# Command that leaves a suggestion for the bot
# p.suggest (suggestion)  
@client.command(aliases=['feedback'])
async def suggest(ctx, *, suggestion = None):
    if suggestion is None:
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Invalid Command Format", value="Try: `p.suggest (suggestion)`", inline=False)
        await ctx.send(embed=embed)
    else:
        # On Suggestion command, ping private discord channel 733592146308890675 with the details
        channelId = client.get_channel(733592146308890675) #suggestions in Plunge Development

        # Response to user's message
        reply=discord.Embed(title="Plunge", color=0xfd5d5d)
        reply.set_thumbnail(url=logourl)
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