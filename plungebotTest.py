import discord
from discord.ext import commands, tasks
import random
import math
import re
import json
import asyncio

####################
# Start Setup
####################

# The prefix for all the commands
prefix = "p."

# All active battles for a server
activeBattles = []

# All active users in a battle
activeUsers = []

# Sets the bots prefix and removes the help command for our own custom help command
client = commands.Bot(command_prefix = prefix, case_insensitive=True)
client.remove_command('help')

# The url for our logo
logourl = "https://i.imgur.com/tdbgl13.png"

# Reads the Auth.json File
with open('json/auth.json', 'r') as f:
    data = json.load(f)

# Displays that the bot is ready and loops through its statuses
@client.event
async def on_ready():
    client.loop.create_task(change_status())
    print('Bot is ready.')

####################
# End Setup
####################

# TODO: Re-write some of the Embed Messages

# TODO: Make the shop command (with scrolling pages Contact Me before you start)

# TODO: Make the loadout command (Lets you choose your loadout weapons)

# TODO: Make the perk command (Lets you choose your perk to equip)

# TODO: Make the showcase command (Lets you choose what to display in your showcase.. Pickaxes, weapons, umbrellas, perks)

# TODO: Make the title command (Lets you equip one of your titles that you own)

# TODO: Make the leaderboard command (Displays the top 100 players for wins/gold/level)

####################
# Start Bot Methods
####################

# Updates and cycles the bots status
async def change_status():
    while True:
        # await client.change_presence(
        #     activity=discord.Game('Dropped ' + str(await getInfo('drops')) + " times!")
        # )

        # await asyncio.sleep(15)

        guilds = str(len([g for g in client.guilds]))  # Gets length of all client's guilds
        
        users = 0
        for guild in client.guilds:
            users += len(guild.members)        # Gets how many users are in all of the guilds combined

        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=f"s: {guilds} • u: {users}")
        )

        await asyncio.sleep(15)

        await client.change_presence(
            activity=discord.Game(' p.help • p.verify • p.invite')
        )

        await asyncio.sleep(15)

        await client.change_presence(
            activity=discord.Game('Hosted ' + str(await getInfo('battles')) + " battles!")
        )

        await asyncio.sleep(15)

        await client.change_presence(
            activity=discord.Game(' p.battle • p.profile • p.shop')
        )

        await asyncio.sleep(15)

# Checks if the authorId is a dev's authorId
def isDev(authorId):
    if authorId == 260698008595726336 or authorId == 534099020230950923 or authorId == 290530439331053579:
        return True 
    else:
        return False

####################
# End Bot Methods
####################

####################
# Start Get Methods
####################

# Gets the bots drop count or the bots battle count
async def getInfo(info):
    with open('json/info.json', 'r') as f:
        drops = json.load(f)
    
    return drops[info]

# Function to get the keys (users ID) from the userInfo.json
async def getKeys(json):
    items = []
    for key, value in json:
        items.append(key)

    return items

# Function to get the values (server ID) from the userInfo.json
async def getValues(json):
    items = []
    for key, value in json:
        items.append(value)
    
    return items

# Function to get the weapons Rarity
async def getRarity(rarityId):
    with open('json/rarity.json', 'r') as f:
        rarity = json.load(f)

    return rarity[str(rarityId)]

# Function to get the weapons Range
async def getRange(rangeId):
    with open('json/ranges.json', 'r') as f:
        ranges = json.load(f)

    return ranges[str(rangeId)]

####################
# End Get Methods
####################

####################
# Start Add Methods
####################

# Adds to the drop counter
async def addDrop():
    with open('json/info.json', 'r') as f:
        drops = json.load(f)
        
        drops["drops"] += 1

        with open('json/info.json', 'w') as f:
            json.dump(drops, f, indent=4)

# Adds to the battle counter
async def addBattle():
    with open('json/info.json', 'r') as f:
        battles = json.load(f)
        
        battles["battles"] += 1

        with open('json/info.json', 'w') as f:
            json.dump(battles, f, indent=4)


####################
# End Add Methods
####################

####################
# Start User Helper Methods
####################

### Add and Remove Currency ###
# Add gold
async def addGold(userId, gold):
    with open('json/users.json', 'r') as f:
        data = json.load(f)
    
    data[str(userId)]['inventory']['gold'] += gold

    with open('json/users.json', 'w') as f:
        json.dump(data, f, indent=4)

# Add gems
async def addGems(userId, gems):
    with open('json/users.json', 'r') as f:
        data = json.load(f)
    
    data[str(userId)]['inventory']['gems'] += gems

    with open('json/users.json', 'w') as f:
        json.dump(data, f, indent=4)

# Remove gold
async def removeGold(userId, gold):
    with open('json/users.json', 'r') as f:
        data = json.load(f)
    
    data[str(userId)]['inventory']['gold'] -= gold

    with open('json/users.json', 'w') as f:
        json.dump(data, f, indent=4)

# Remove gems
async def removeGems(userId, gems):
    with open('json/users.json', 'r') as f:
        data = json.load(f)
    
    data[str(userId)]['inventory']['gems'] -= gems

    with open('json/users.json', 'w') as f:
        json.dump(data, f, indent=4)

####################
# End User Helper Methods
####################

####################
# Start Weapon Helper Methods
####################

####################
# End Weapon Helper Methods
####################

####################
# Start Client Event Methods
####################

# When the bot is directly mentioned "@Plunge", give a description about what the bot is about
@client.event
async def on_message(message):
    if message.content == '<@!732864657932681278>':
        embed=discord.Embed(title="Plunge", description=f"Hey {message.author.mention}, can't decide on where to drop in Fortnite? It happens to us all, we  are riding in the battle bus with our maps open but no location marked.  Before we know it, we are getting kicked off the bus with little to no options to land. Luckily, Plunge Bot can help. With a simple command `p.drop`, Plunge will randomly select a location for you to drop in Fortnite, making your next drop stress free.", color=0xfd5d5d)
        embed.add_field(name="!! Special !!", value="We are currently hosting a giveaway!\nDo `p.giveaway` for information on how to qualify.",inline=False)
        embed.add_field(name="Info", value="Use `p.help` to get started", inline=False)
        embed.set_thumbnail(url=logourl)
        embed.set_footer(text="Created by The Plunge Team")
        await message.channel.send(embed=embed)
    await client.process_commands(message)

# On guild removed, it removes the users role in Plunge development and removes them from the userInfo.json and sends the users effected a dm.
@client.event
async def on_guild_remove(guild):
    ourGuild = client.get_guild(733551377611096195)

    with open('json/userInfo.json', 'r') as f:
        userInfo = json.load(f)

    for key, value in list(userInfo.items()):
        if (value == str(guild.id)):
            userInfo.pop(key)

            with open('json/userInfo.json', 'w') as f:
                json.dump(userInfo, f, indent=4)

            await ourGuild.get_member(int(key)).remove_roles(ourGuild.get_role(733559654210207885), reason="They removed the bot from their server.")
            await ourGuild.get_member(int(key)).add_roles(ourGuild.get_role(733558248401272832), reason="They removed the bot from their server.")

            embed=discord.Embed(title="Plunge", color=0xfd5d5d)
            embed.set_thumbnail(url=logourl)
            embed.add_field(name="Verification Revoked", value="Hey, looks like you are no longer verified. The bot is no longer in the server you were verified in. Unfortunately, you have lost the User role in the Plunge Development server.\n\nYou can [invite the bot](https://discord.com/api/oauth2/authorize?client_id=732864657932681278&permissions=313408&scope=bot) to another server and use the `p.verify` command to get back the User role.", inline=False)

            await ourGuild.get_member(int(key)).send(embed=embed)

####################
# End Client Event Methods
####################

####################
# Start Bot Commands
####################

# Help Command
# p.help
# @client.command()
# async def help(ctx, setting = None):
#     if setting is None:
#         embed=discord.Embed(title="Plunge", description="List of Commands", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="General", value=f"`{prefix}drop` `{prefix}battle` `{prefix}help` `{prefix}feedback` `{prefix}invite` `{prefix}discord` `{prefix}verify` `{prefix}giveaway`", inline=False)
#         embed.add_field(name="Info", value=f"To get more help on a command or see the command's function, try: `p.help (command)`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "drop":
#         embed=discord.Embed(title="Plunge", description="Drop Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Gives you a random location to drop in Fortnite!", inline=False)
#         embed.add_field(name="Usage:", value="`p.drop`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "battle":
#         embed=discord.Embed(title="Plunge", description="Battle Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Starts a simulated battle royale for your server.", inline=False)
#         embed.add_field(name="Usage:", value="`p.battle`", inline=False)
#         embed.set_footer(text="p.stats • view your battle royale stats")
#         await ctx.send(embed=embed)
#     elif setting.lower() == "suggest":
#         embed=discord.Embed(title="Plunge", description="Suggest Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Sends your suggestion to the developers to review.", inline=False)
#         embed.add_field(name="Usage:", value="`p.suggest (your suggestion)`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "feedback":
#         embed=discord.Embed(title="Plunge", description="Feedback Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Sends your feedback for the developers to review.", inline=False)
#         embed.add_field(name="Usage:", value="`p.feedback (your feedback)`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "invite":
#         embed=discord.Embed(title="Plunge", description="Invite Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Gives you a link to invite this bot to your server!", inline=False)
#         embed.add_field(name="Usage:", value="`p.invite`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "discord":
#         embed=discord.Embed(title="Plunge", description="Discord Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Invites you to the bot's development server!", inline=False)
#         embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
#         embed.add_field(name="Aliases:", value="`p.server`, `p.join`, `p.support`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "server":
#         embed=discord.Embed(title="Plunge", description="Server Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Invites you to the bot's development server!", inline=False)
#         embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
#         embed.add_field(name="Aliases:", value="`p.discord`, `p.join`, `p.support`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "join":
#         embed=discord.Embed(title="Plunge", description="Join Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Invites you to the bot's development server!", inline=False)
#         embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
#         embed.add_field(name="Aliases:", value="`p.discord`, `p.server`, `p.support`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "support":
#         embed=discord.Embed(title="Plunge", description="Support Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Invites you to the bot's development server!", inline=False)
#         embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
#         embed.add_field(name="Aliases:", value="`p.discord`, `p.server`, `p.join`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "verify":
#         embed=discord.Embed(title="Plunge", description="Verify Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Verifies that you have the bot in your server, giving you the User Role in the Plunge Development server.", inline=False)
#         embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
#         await ctx.send(embed=embed)
#     elif setting.lower() == "giveaway":
#         embed=discord.Embed(title="Plunge", description="Giveaway Command", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Description:", value=f"Displays information about the current giveaway.", inline=False)
#         embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
#         await ctx.send(embed=embed)
#     else:
#         embed=discord.Embed(title="Plunge", description="Invalid Command Setting", color=0xfd5d5d)
#         embed.set_thumbnail(url=logourl)
#         embed.add_field(name="Try:", value=f"`p.help` or `p.help (command)`", inline=False)
#         await ctx.send(embed=embed)

@client.command()
async def help(ctx):
    commands = f"`p.info` Gives instructions on how to use this bot\n`p.battle` Starts a battle royale\n`p.shop` Displays the current shop items\n`p.profile` Shows your profile\n`p.inventory` Shows your inventory\n`p.chest` Opens a chest which contains gold and items\n`p.loadout` Pick your loadout items\n`p.perk` Pick a perk to equip\n`p.showcase` Pick your showcase items\n`p.title` Pick a title to equip\n`p.color` At level 100, change your profile color\n`p.leaderboard` Shows some of the best battle royale players\n`p.invite` Sends an invite link to have the bot join your own server\n`p.discord` Sends an invite link to join our discord server\n`p.verify` Gives you the user role in our discord server\n`p.giveaway` Gives information about the active giveaway"

    embed=discord.Embed(title="Plunge Help Page", color=0xfd5d5d)
    embed.set_thumbnail(url=logourl)
    embed.add_field(name="List of Commands", value=f"{commands}", inline=False)
    embed.add_field(name="Have feedback for us?", value=f"Use `p.feedback [your message]` to let us know what you would like to see in the future.", inline=False)
    await ctx.send(embed=embed)

# Command to let the user know where to drop using the drop command
# Can't decide on where to drop in Fortnite? It happens to us all, we  are riding in the battle bus with our maps open but no location marked.  
# Before we know it, we are getting kicked off the bus with little to no options to land. Luckily, Plunge Bot can help. With a simple command 
# "p.drop", Plunge will randomly select a location for you to drop in Fortnite, making your next drop stress free.
# p.drop
# @client.command()
# async def drop(ctx):
#     # Call the add drop command to add to the counter
#     await addDrop()

#     # Removed: "The Shark"
#     locations = ['Catty Corner', 'Frenzy Farm', 'Holly Hedges', 'Lazy Lake', 'Misty Meadows', 'Pleasant Park', 'Retail Row', 'Rickety Rig', 'Salty Springs', 'Steamy Stacks', 'Sweaty Sands', 'The Authority', 'The Fortilla', 'Risky Reels', 'The Yacht', 'Dirty Docks', 'Broken Castle', 'Pirate Barge']
#     location = random.choice(locations)

#     # locationurl = f'http://www.genplus.xyz/plunge/images/{location.replace(" ", "%20")}.png'
#     locationurl = ''

#     # Based on the location, set the image url
#     if location == 'Catty Corner':
#         locationurl = 'https://i.imgur.com/IN3zcJJ.png'
#     elif location == 'Frenzy Farm':
#         locationurl = 'https://i.imgur.com/c1pYdgs.png'
#     elif location == 'Holly Hedges':
#         locationurl = 'https://i.imgur.com/GX2A97E.png'
#     elif location == 'Lazy Lake':
#         locationurl = 'https://i.imgur.com/cNlKs5b.png'
#     elif location == 'Misty Meadows':
#         locationurl = 'https://i.imgur.com/QneWdkB.png'
#     elif location == 'Pleasant Park':
#         locationurl = 'https://i.imgur.com/cuIXiTM.png'
#     elif location == 'Retail Row':
#         locationurl = 'https://i.imgur.com/sIuNMV4.png'
#     elif location == 'Rickety Rig':
#         locationurl = 'https://i.imgur.com/tsJPpyn.png'
#     elif location == 'Salty Springs':
#         locationurl = 'https://i.imgur.com/KBFUFPN.png'
#     elif location == 'Steamy Stacks':
#         locationurl = 'https://i.imgur.com/QLPw5Bb.png'
#     elif location == 'Sweaty Sands':
#         locationurl = 'https://i.imgur.com/9eQBa08.png'
#     elif location == 'The Authority':
#         locationurl = 'https://i.imgur.com/JXWhuzJ.png'
#     elif location == 'The Fortilla':
#         locationurl = 'https://i.imgur.com/EOeio4u.png'
#     elif location == 'Risky Reels':
#         locationurl = 'https://i.imgur.com/K6Zwis8.png'
#     elif location == 'The Yacht':
#         locationurl = 'https://i.imgur.com/OLyro4T.png'
#     elif location == 'Dirty Docks':
#         locationurl = 'https://i.imgur.com/sPrr5rY.png'
#     elif location == 'Broken Castle':
#         locationurl = 'https://i.imgur.com/DocMZvk.png'
#     elif location == 'Pirate Barge':
#         locationurl = 'https://i.imgur.com/qpcf2bd.png'
#     else:
#         locationurl = ''

#     embed=discord.Embed(title="Plunge", color=0xfd5d5d)
#     embed.add_field(name="You are dropping at:", value=location, inline=False)
#     embed.set_thumbnail(url=logourl)
#     embed.set_image(url=locationurl)
#     await ctx.send(embed=embed)

# Command that simulates a battle royale
# p.battle
@client.command()
async def battle(ctx):
    emoji = client.get_emoji(734656507194507275)

    # If the guild has an active battle royale... tell them.... Else start a battle royale
    if ctx.guild.id in list(activeBattles):
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle In Progress", value="There is already a battle in progress for this server, please wait until the current battle is complete", inline=False)
        progress = await ctx.send(embed=embed)
        await progress.delete(delay=60)
    else:
        # add the guild to the active battles check
        activeBattles.append(ctx.guild.id)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 3 minutes!", inline=False)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('<:plunge:734656507194507275>')

        # await asyncio.sleep(60)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 2 minutes!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(60)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 1 minutes!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(30)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 30 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(10)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 20 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(10)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 10 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(1)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 9 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(1)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 8 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(1)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 7 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(1)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 6 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(1)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 5 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(1)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 4 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(1)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 3 seconds!", inline=False)
        # await msg.edit(embed=embed)

        # await asyncio.sleep(1)

        # embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        # embed.set_thumbnail(url=logourl)
        # embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        # embed.add_field(name="Ready Up!", value="We are starting in 2 seconds!", inline=False)
        # await msg.edit(embed=embed)

        await asyncio.sleep(1)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value=f"React with {emoji} to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 1 seconds!", inline=False)
        await msg.edit(embed=embed)

        # Caches your message so you can get the reactions
        cache_msg = discord.utils.get(client.cached_messages, id = msg.id)
        
        # loops through the reactions
        for reaction in cache_msg.reactions:
            # if reaction is the plunge emoji...
            if str(reaction.emoji) == '<:plunge:734656507194507275>':
                # Grabs the users that used that reaction
                userObjects = await reaction.users().flatten()
                users = []

                # Makes a new list of just user.Id's
                for user in list(userObjects):
                    if user.id != 732864657932681278:
                        users.append(user.id)

                usersToAdd = 20 - len(users)

                if len(users) == 0:
                    # Battle wont start
                    await msg.delete(delay=None)
                    embed=discord.Embed(title="Plunge Error", color=0xfd5d5d)
                    embed.set_thumbnail(url=logourl)
                    embed.add_field(name="Not Enough Players", value=f"Make sure to react to the battle message to be entered in the battle royale.", inline=False)
                    noplayers = await ctx.send(embed=embed)
                    await noplayers.delete(delay=60)
                # If the list is larger than 20 start the battle, else
                elif len(users) > 20:
                    await msg.delete(delay=None)
                    embed=discord.Embed(title="Plunge", color=0xfd5d5d)
                    embed.set_thumbnail(url=logourl)
                    embed.add_field(name="Battle In Progress...", value="Good Luck Everyone!", inline=False)
                    embed.set_footer(text=f"{len(users) - 1} Players")
                    msg = await ctx.send(embed=embed)
                    await msg.delete(delay=60)

                    # Pass the ctx and users list into the battleStart function
                    await battleStart(ctx, users)
                else:
                    await msg.delete(delay=None)
                    embed=discord.Embed(title="Plunge", color=0xfd5d5d)
                    embed.set_thumbnail(url=logourl)
                    embed.add_field(name="Not Enough Players", value=f"Minimum players required: 20\n\nFilling the remaining {usersToAdd} slots with bots", inline=False)
                    msg = await ctx.send(embed=embed)
                    await msg.delete(delay=60)

                    await asyncio.sleep(4)
                    
                    # Add players to the list
                    i = 0
                    while i < usersToAdd:
                        users.append(i)
                        i += 1

                    embed=discord.Embed(title="Plunge", color=0xfd5d5d)
                    embed.set_thumbnail(url=logourl)
                    embed.add_field(name="Battle In Progress...", value="Good Luck Everyone!", inline=False)
                    embed.set_footer(text=f"{len(users)} Players")
                    battleMsg = await ctx.send(embed=embed)

                    await battleMsg.delete(delay=60)

                    # Pass the ctx and users list into the battleStart function
                    await battleStart(ctx, users)

                
        # removes the guild from the active battles check (this comes last)
        activeBattles.remove(ctx.guild.id)

# Command that gets the users profile
# p.profile
@client.command()
async def profile(ctx, args = None):
    # if no parameters, display the authors profile
    if args == None:
        await displayProfile(ctx, ctx.author.id)
    # else, display the passed in user
    else:
        # Format the mentioned user for easy lookup
        args = args.translate(dict.fromkeys(map(ord, '!@<>')))

        # Get the user object
        user = client.get_user(int(args))

        # If user is not None
        if user is not None:
            # Display passed in user
            await displayProfile(ctx, user.id)
        else:
            print("User not found. Profile Command.")
            # Don't purchase the item
            embed=discord.Embed(color=0xfd5d5d)
            embed.add_field(name="**User Not Found**", value=f"Make sure you are looking up someone from the server you are in.", inline=False)
            failed = await ctx.send(embed=embed)
            await failed.delete(delay=60)

# Displays the users profile
async def displayProfile(ctx, userId):
    # Get the user
    user = client.get_user(userId)

    # Fetch the user from the list
    userProfile = await fetchUserProfile(userId)

    if userProfile is True:
        await ctx.send(f"{user.name}#{user.discriminator} has not yet played in a Battle Royale... Creating User...")
    else:

        # Get the users profile info
        name = userProfile["name"]

        titleId = userProfile["title"]
        title = await fetchTitleName(titleId)

        showcase1Id = userProfile["showcase1"]
        showcase2Id = userProfile["showcase2"]
        showcase3Id = userProfile["showcase3"]
        showcase1 = await fetchItem(showcase1Id)
        showcase2 = await fetchItem(showcase2Id)
        showcase3 = await fetchItem(showcase3Id)
        
        showcase1Emoji = client.get_emoji(showcase1["emojiId"])
        showcase1Name = showcase1["name"]

        showcase2Emoji = client.get_emoji(showcase2["emojiId"])
        showcase2Name = showcase2["name"]

        showcase3Emoji = client.get_emoji(showcase3["emojiId"])
        showcase3Name = showcase3["name"]

        wins = userProfile["stats"]["wins"]
        kills = userProfile["stats"]["kills"]
        deaths = userProfile["stats"]["deaths"]
        kd = await calcKD(kills, deaths)
        level = math.floor(userProfile["stats"]["totalExp"]/100)
        gamesPlayed = deaths + wins
        winPerc = await calcWinPerc(wins, gamesPlayed)

        pickaxeId = userProfile["loadout"]["pickaxe"]
        slot1Id = userProfile["loadout"]["slot1"]
        slot2Id = userProfile["loadout"]["slot2"]
        slot3Id = userProfile["loadout"]["slot3"]
        slot4Id = userProfile["loadout"]["slot4"]
        perkId = userProfile["loadout"]["perk"]
        pickaxe = await fetchItem(pickaxeId)
        slot1 = await fetchItem(slot1Id)
        slot2 = await fetchItem(slot2Id)
        slot3 = await fetchItem(slot3Id)
        slot4 = await fetchItem(slot4Id)
        perk = await fetchItem(perkId)

        pickaxeName = pickaxe["name"]
        pickaxeEmoji = client.get_emoji(pickaxe["emojiId"])
        slot1Name = slot1["name"]
        slot1Emoji = client.get_emoji(slot1["emojiId"])
        slot1Rarity = await getRarity(slot1["rarityId"])
        slot1Threat = slot1Rarity["threat"]
        threat1 = slot1Threat
        if slot1Threat == 0:
            slot1Threat = ""
        else:
            slot1Threat = f"`+{slot1Threat * 10} threat`"

        slot2Name = slot2["name"]
        slot2Emoji = client.get_emoji(slot2["emojiId"])
        slot2Rarity = await getRarity(slot2["rarityId"])
        slot2Threat = slot2Rarity["threat"]
        threat2 = slot2Threat
        if slot2Threat == 0:
            slot2Threat = ""
        else:
            slot2Threat = f"`+{slot2Threat * 10} threat`"

        slot3Name = slot3["name"]
        slot3Emoji = client.get_emoji(slot3["emojiId"])
        slot3Rarity = await getRarity(slot3["rarityId"])
        slot3Threat = slot3Rarity["threat"]
        threat3 = slot3Threat
        if slot3Threat == 0:
            slot3Threat = ""
        else:
            slot3Threat = f"`+{slot3Threat * 10} threat`"

        slot4Name = slot4["name"]
        slot4Emoji = client.get_emoji(slot4["emojiId"])
        slot4Rarity = await getRarity(slot4["rarityId"])
        slot4Threat = slot4Rarity["threat"]
        threat4 = slot4Threat
        if slot4Threat == 0:
            slot4Threat = ""
        else:
            slot4Threat = f"`+{slot4Threat * 10} threat`"

        perkName = perk["name"]
        perkEmoji = client.get_emoji(perk["emojiId"])
        perkBonus = await getPerkBonus(perkId)

        totalWeapons = len(userProfile["inventory"]["weapons"])
        totalPerks = len(userProfile["inventory"]["perks"])
        totalUmbrellas = len(userProfile["inventory"]["umbrellas"])
        totalTitles = len(userProfile["inventory"]["titles"])
        totalChests = userProfile["inventory"]["chests"]
        totalPickaxes = len(userProfile["inventory"]["pickaxes"])
        inventorySize = totalWeapons + totalPerks + totalUmbrellas + totalTitles + totalChests + totalPickaxes

        gold = userProfile["inventory"]["gold"]
        gems = userProfile["inventory"]["gems"]
        goldEmoji = client.get_emoji(736439923095109723)
        gemEmoji = client.get_emoji(736451870016405655)

        totalThreat = threat1 + threat2 + threat3 + threat4

        if perkId == 1000:
            totalThreat = totalThreat + 2

        # Sets Color based off level
        if level < 10:
            color = 2433568
        elif level > 9 and level < 20:
            color = 14885182
        elif level > 19 and level < 30:
            color = 16407354
        elif level > 29 and level < 40:
            color = 16764160
        elif level > 39 and level < 50:
            color = 31530
        elif level > 49 and level < 60:
            color = 37347
        elif level > 59 and level < 70:
            color = 8476113
        elif level > 69 and level < 80:
            color = 14702034
        elif level > 79 and level < 90:
            color = 6363698
        elif level > 89 and level < 100:
            color = 14673631
        elif level >= 100:
            color = int(userProfile["color"], 16)

        embed=discord.Embed(title=f"{name}\'s Profile", color=color)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name=f"Level: {level}\nThreat: {totalThreat * 10}", value=f"{title} {name}#{user.discriminator}\n\n**Gold:** {gold} {goldEmoji}\n**Gems:** {gems} {gemEmoji}\n\n ", inline=False),
        embed.add_field(name=f"__Stats__", value=f"Wins: {wins}\nKills: {kills}\nDeaths: {deaths}\nK/D Ratio: {kd}\nGames Played: {gamesPlayed}\nWin Percent: {winPerc}%\n\n", inline=True)
        embed.add_field(name=f"__Showcase__", value=f"{showcase1Emoji} {showcase1Name}\n{showcase2Emoji} {showcase2Name}\n{showcase3Emoji} {showcase3Name}", inline=True)
        embed.add_field(name=f"__Pickaxe__", value=f"{pickaxeEmoji} {pickaxeName}\n", inline=False)
        embed.add_field(name=f"__Loadout__", value=f"**1.** {slot1Emoji} {slot1Name} {slot1Threat}\n**2.** {slot2Emoji} {slot2Name} {slot2Threat}\n**3.** {slot3Emoji} {slot3Name} {slot3Threat}\n**4.** {slot4Emoji} {slot4Name} {slot4Threat}\n", inline=False)
        embed.add_field(name=f"__Perk__", value=f"{perkEmoji} {perkName} {perkBonus}", inline=False)        
        embed.set_footer(text=f"Inventory ({inventorySize})")
        await ctx.send(embed=embed)

# Fetches the user.. if not found, creates a new user
async def fetchUserProfile(userId):
    # Opens the users.json file and reads it
    with open('json/users.json', 'r') as f:
        userData = json.load(f)

    # Checks if userId is in the userData list
    if str(userId) in list(userData.keys()):
        # update the users name
        updateName(userId)
        # return the user
        return userData[str(userId)]
    # else create new user
    else:
        # Creates a user
        await createNewUser(userId)
        return True

# Fetches The Title Name
async def fetchTitleName(titleId):
    # Opens the titles.json
    with open('json/titles.json', 'r') as f:
        titleData = json.load(f)

    if str(titleId) in list(titleData.keys()):
        title = titleData[str(titleId)]["title"]
        
        if title != "":
            title = "`[" + title + "]`"

        return title
    else:
        print("Title name not found. fetchTitleName error.")

# Fetchs an item based on its ID
async def fetchItem(itemId):
    if itemId < 1000:
        with open('json/weapons.json', 'r') as f:
            weaponData = json.load(f)

        if str(itemId) in list(weaponData.keys()):
            return weaponData[str(itemId)]
        else:
            print("Weapon not found. fetchItem error.")
    elif itemId > 999 and itemId < 2000:
        with open('json/perks.json', 'r') as f:
            perkData = json.load(f)

        if str(itemId) in list(perkData.keys()):
            return perkData[str(itemId)]
        else:
            print("Perk not found. fetchItem error.")
    elif itemId > 1999 and itemId < 3000:
        with open('json/umbrellas.json', 'r') as f:
            umbrellaData = json.load(f)

        if str(itemId) in list(umbrellaData.keys()):
            return umbrellaData[str(itemId)]
        else:
            print("Umbrella not found. fetchItem error.")
    elif itemId > 2999 and itemId < 4000:
        with open('json/titles.json', 'r') as f:
            titleData = json.load(f)

        if str(itemId) in list(titleData.keys()):
            return titleData[str(itemId)]
        else:
            print("Title not found. fetchItem error.")
    elif itemId > 3999 and itemId < 5000:
        with open('json/chests.json', 'r') as f:
            chestData = json.load(f)

        if str(itemId) in list(chestData.keys()):
            return chestData[str(itemId)]
        else:
            print("Chest not found. fetchItem error.")
    else:
        with open('json/pickaxes.json', 'r') as f:
            pickData = json.load(f)

        if str(itemId) in list(pickData.keys()):
            return pickData[str(itemId)]
        else:
            print("Pick not found. fetchItem error.")

# Adds an item to the users inventory
async def addItem(userId, itemId):
    with open('json/users.json', 'r') as f:
        data = json.load(f)

    if itemId < 1000:
        # Add the weapon to the users inventory
        if itemId in data[str(userId)]['inventory']['weapons']:
            print(f'The item is already in {userId} inventory')
            return True
        else:
            data[str(userId)]['inventory']['weapons'].append(itemId)

    elif itemId > 999 and itemId < 2000:
        # Add the perk to the users inventory
        if itemId in data[str(userId)]['inventory']['perks']:
            print(f'The item is already in {userId} inventory')
        else:
            data[str(userId)]['inventory']['perks'].append(itemId)

    elif itemId > 1999 and itemId < 3000:
        # Add an umbrealla to the users inventory
        if itemId in data[str(userId)]['inventory']['umbrellas']:
            print(f'The item is already in {userId} inventory')
        else:
            data[str(userId)]['inventory']['umbrellas'].append(itemId)

    elif itemId > 2999 and itemId < 4000:
        # Add a title to the users inventory
        if itemId in data[str(userId)]['inventory']['titles']:
            print(f'The item is already in {userId} inventory')
        else:
            data[str(userId)]['inventory']['titles'].append(itemId)

    elif itemId > 3999 and itemId < 5000:
        # Add a chest to the users inventory
        # DO NOTHING
        return False
    else:
        # Add a pickaxe to the users inventory
        if itemId in data[str(userId)]['inventory']['pickaxes']:
            print(f'The item is already in {userId} inventory')
        else:
            data[str(userId)]['inventory']['pickaxes'].append(itemId)

    with open('json/users.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    return False

# Update the users name field
def updateName(userId):
    with open('json/users.json', 'r') as f:
        data = json.load(f)
    
    user = client.get_user(userId)

    if user != None:
        data[str(userId)]['name'] = user.name
    
    with open('json/users.json', 'w') as f:
        json.dump(data, f, indent=4)

# Create a new user in the users.json
async def createNewUser(userId):
    # Opens the users.json file and read it
    with open('json/users.json', 'r') as f:
        userData = json.load(f)
    
    # If user is not in the list, add a new user
    if str(userId) not in list(userData.keys()):
        # Gets the users name
        user = client.get_user(userId)

        stats = {
            "wins": 0,
            "kills": 0,
            "deaths": 0,
            "totalExp": 0
        }

        matchStats = {}

        loadout = {
            "pickaxe": 5000,
            "slot1": 999,
            "slot2": 999,
            "slot3": 999,
            "slot4": 999,
            "perk": 1999
        }
        inventory = {
            "weapons": [],
            "perks": [],
            "umbrellas": [],
            "titles": [],
            "chests": 0,
            "pickaxes": [5000],
            "gold": 250,
            "gems": 0
        }

        userData[str(userId)] = {
            "name": user.name,
            "title": 3999,
            "color": "0c0d0c",
            "showcase1": 999,
            "showcase2": 999,
            "showcase3": 999,
            "stats": stats,
            "matchStats": matchStats,
            "loadout": loadout,
            "inventory": inventory
        }
    
        with open('json/users.json', 'w') as f:
            json.dump(userData, f, indent=4)

async def addMatchStats(userId, serverId):
    # Opens the users.json file and read it
    with open('json/users.json', 'r') as f:
        userData = json.load(f)

    userData[str(userId)]["matchStats"][str(serverId)] = {
        "placement": 0,
        "killsEarned": 0,
        "goldEarned": 0,
        "expEarned": 0,
        "itemsEarned": []
    }

    with open('json/users.json', 'w') as f:
        json.dump(userData, f, indent=4)

# Get the users kill death ratio
async def calcKD(kills, deaths):
    if kills > 0 and deaths > 0:
        kd = kills / deaths
    elif deaths == 0:
        kd = kills
    else:
        kd = 0

    return round(kd, 2)

# Get the users win percentage
async def calcWinPerc(wins, gamesPlayed):
    if wins > 0 and gamesPlayed > 0:
        winperc = wins / gamesPlayed * 100
    else:
        winperc = 0

    return round(winperc)

# Gets the bonus of the perk you have equipped
async def getPerkBonus(perkId):
    if perkId == 1999:
        return ""
    elif perkId == 1000:
        return "`+20 Threat`"
    elif perkId == 1001:
        return "`+10% Gold`"
    elif perkId == 1002:
        return "`+10% Exp`"

# Command that sets the users profile color
@client.command()
async def color(ctx, color = None):
    with open('json/users.json', 'r') as f:
        data = json.load(f)

    usersExp = data[str(ctx.author.id)]['stats']['totalExp']
    usersLevel = math.floor(usersExp/100)

    if color != None:
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)

    if usersExp < 10000:
        embed=discord.Embed(title=f"Not High Enough Level", description=f"Sorry {ctx.author.name}, you must be level 100 in order to change the color of your profile page.\n\nCurrent Level: {usersLevel}", color=0xfd5d5d)
        await ctx.send(embed=embed)
    else:
        if color == None:
            embed=discord.Embed(title=f"No color provided", description=f"To change the color of your profile, provide a valid hex color code.\nYou can choose a color from [here](https://www.google.com/search?q=color+picker).\n\nExample: `p.color #1bde2e`", color=0xfd5d5d)
            await ctx.send(embed=embed)
        elif match:
            colorToAdd = color.replace('#', '')
            data[str(ctx.author.id)]['color'] = colorToAdd

            with open('json/users.json', 'w') as f:
                json.dump(data, f, indent=4)

            profileColor = int(colorToAdd, 16)

            embed=discord.Embed(title=f"Color Changed", description=f"{ctx.author.mention}\\'s profile color changed to {color}", color=profileColor)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=f"Invalid Color", description=f"Please provide a valid hex color code. You can choose a color [here](https://www.google.com/search?q=color+picker).", color=0xfd5d5d)
            await ctx.send(embed=embed)

# Command that gets the users inventory #TODO: Rework it, so the items are organized and also get their items ID attached to the end of the string. Also Include the gold, gem, chest emoji
# p.inventory
@client.command()
async def inventory(ctx):
    # Fetch the user from the list
    userProfile = await fetchUserProfile(ctx.author.id)

    if userProfile is True:
        await ctx.send(f"{ctx.author.name}#{ctx.author.discriminator} does not have an inventory yet... Creating User...")
    else:
        # Get the users profile info
        name = userProfile["name"]

        titleId = userProfile["title"]
        title = await fetchTitleName(titleId)

        weaponList = userProfile["inventory"]["weapons"]
        perkList = userProfile["inventory"]["perks"]
        umbrellaList = userProfile["inventory"]["umbrellas"]
        titleList = userProfile["inventory"]["titles"]
        chests = userProfile["inventory"]["chests"]
        pickaxeList = userProfile["inventory"]["pickaxes"]
        gold = userProfile["inventory"]["gold"]
        gems = userProfile["inventory"]["gems"]

        # returns a string based on the weapons in the list
        weapons = fetchWeapons(weaponList)
        perks = fetchPerks(perkList)
        umbrellas = fetchUmbrellas(umbrellaList)
        titles = fetchTitles(titleList)
        pickaxes = fetchPickaxes(pickaxeList)

        embed=discord.Embed(title=f"{title} {name}\'s Inventory", color=0xfd5d5d)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name=f"__Weapons__", value=f"{weapons}", inline=False)
        embed.add_field(name=f"__Pickaxes__", value=f"{pickaxes}", inline=False)
        embed.add_field(name=f"__Perks__", value=f"{perks}", inline=False)
        embed.add_field(name=f"__Umbrellas__", value=f"{umbrellas}", inline=False)
        embed.add_field(name=f"__Titles__", value=f"{titles}\n\n**Gold:** {gold}\n**Gems:** {gems}\n**Chests:** {chests}", inline=False)
        await ctx.send(embed=embed)

# Takes a list of weapons and returns a formated string
def fetchWeapons(weapons):
    value = ''

    with open('json/weapons.json', 'r') as f:
        data = json.load(f)

    with open('json/rarity.json', 'r') as r:
        rarity = json.load(r)

    for weaponId in weapons:
        emojiId = data[str(weaponId)]['emojiId']
        emoji = client.get_emoji(emojiId)
        name = data[str(weaponId)]['name']
        rarityId = data[str(weaponId)]['rarityId']
        threat = rarity[str(rarityId)]['threat'] * 10

        value += f'{emoji} {name} `+{threat} threat` [*#{weaponId}*]\n'
    
    if value == '':
        return 'None'
    else:
        return value

# Takes a weaponID and returns a formated string
def fetchWeapon(weaponId):
    value = ''

    with open('json/weapons.json', 'r') as f:
        data = json.load(f)

    with open('json/rarity.json', 'r') as r:
        rarity = json.load(r)

    emojiId = data[str(weaponId)]['emojiId']
    emoji = client.get_emoji(emojiId)
    name = data[str(weaponId)]['name']
    rarityId = data[str(weaponId)]['rarityId']
    threat = rarity[str(rarityId)]['threat'] * 10

    value += f'{emoji} {name} `+{threat} threat`'
    
    return value


# Takes a list of perks and returns a formated string
def fetchPerks(perks):
    value = ''

    with open('json/perks.json', 'r') as f:
        data = json.load(f)
    
    for perkId in perks:
        emojiId = data[str(perkId)]['emojiId']
        emoji = client.get_emoji(emojiId)
        name = data[str(perkId)]['name']

        if perkId == 1000:
            bonus = f'`+20 threat`'
        elif perkId == 1001:
            bonus = f'`+10% gold`'
        elif perkId == 1002:
            bonus = f'`+10% exp`'

        value += f'{emoji} {name} {bonus} [*#{perkId}*]\n'

    if value == '':
        return 'None'
    else:
        return value

# Takes a list of umbrellas and returns a formated string
# TODO: update the umbrella emoji's
def fetchUmbrellas(umbrellas):
    value = ''

    with open('json/umbrellas.json', 'r') as f:
        data = json.load(f)

    for umbrellaId in umbrellas:
        emojiId = data[str(umbrellaId)]['emojiId']
        # Get emoji here
        name = data[str(umbrellaId)]['name']

        value += f'{name} [*#{umbrellaId}*]\n'

    if value == '':
        return 'None'
    else:
        return value

# Takes a list of titles and returns a formated string
def fetchTitles(titles):
    value = ''

    with open('json/titles.json', 'r') as f:
        data = json.load(f)

    for titleId in titles:
        name = data[str(titleId)]['title']

        value += f'`{name}` [*#{titleId}*]\n'

    if value == '':
        return 'None'
    else:
        return value


# Takes a list of pickaxes and returns a formated string
def fetchPickaxes(pickaxes):
    value = ''

    with open('json/pickaxes.json', 'r') as f:
        data = json.load(f)

    for pickaxeId in pickaxes:
        emojiId = data[str(pickaxeId)]['emojiId']
        emoji = client.get_emoji(emojiId)
        name = data[str(pickaxeId)]['name']

        value += f'{emoji} {name} [*#{pickaxeId}*]\n'

    if value == '':
        return 'None'
    else:
        return value


####################
# End Bot Commands
####################

####################
# Start Mod Commands
####################

@client.command()
async def updates(ctx):
    if isDev(ctx.author.id):
        updates = client.get_channel(733858209046986863) # Gets #updates channel in Plunge Development
        embed=discord.Embed(title="Plunge (BETA v1.0.0)", description="Bot Released with features", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Added", value="`p.drop` - Gives a random location to drop in Fortnite!\n`p.battle` - Starts a simulated battle royale for your server.\n`p.help` - Shows a list of all commands\n", inline=False)
        await updates.send(embed=embed)
    else:
        # If people are trying to use this command and are not dev, tell them its an unknown command
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Command Not Found", value="Try `p.help` for a list of all commands.", inline=False)
        await ctx.send(embed=embed)

####################
# End Mod Commands
####################

# Command to invite the bot to your server
# p.invite
@client.command()
async def invite(ctx):
    embed=discord.Embed(title="Plunge Invite Link", description="If you'd like to invite this bot to your own server, [click here](https://discord.com/api/oauth2/authorize?client_id=732864657932681278&permissions=288832&scope=bot) for an invite", color=0xfd5d5d)
    embed.set_thumbnail(url=logourl)
    await ctx.send(embed=embed)

# Command to see how many servers the bot is in
# p.servers, p.botservers, p.botserver
@client.command(aliases=['botservers', 'botserver'])
async def servers(ctx):
    embed=discord.Embed(title="Plunge", color=0xfd5d5d)
    embed.set_thumbnail(url=logourl)
    embed.add_field(name="Plunge is in:", value=f"{str(len(client.guilds))} servers", inline=False)
    for guild in client.guilds:
        print(guild.name)
    await ctx.send(embed=embed)

# Command to verify they added the bot to the server
# p.verify
@client.command()
@commands.has_guild_permissions(manage_guild=True)
async def verify(ctx):
    # print(ctx.guild.get_member(ctx.author.id).guild_permissions) # This returns the value of your permissions Elyxirs -> value=2147483647
    ourGuild = client.get_guild(733551377611096195)

    users = []

    for user in ourGuild.members:
        users.append(user.id)

    if (ctx.author.id in users):
        await ourGuild.get_member(ctx.author.id).add_roles(ourGuild.get_role(733559654210207885), reason="Used the verify command")
        await ourGuild.get_member(ctx.author.id).remove_roles(ourGuild.get_role(733558248401272832), reason="Used the verify command")

        with open('json/userInfo.json', 'r') as f:
            userInfo = json.load(f)

        keys = await getKeys(userInfo.items())

        # if the user is already verified tell them... else verify them
        if (str(ctx.author.id) in keys):
            embed=discord.Embed(title="Plunge", color=0xfd5d5d)
            embed.set_thumbnail(url=logourl)
            embed.add_field(name="Already Verified", value=f"{ctx.author.mention}, you are already verified and have the User role in the Plunge Development server.\n\nHead over to the Plunge Development server to see!", inline=False)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Plunge", color=0xfd5d5d)
            embed.set_thumbnail(url=logourl)
            embed.add_field(name=f"Verified", value=f"{ctx.author.mention}, you are now verified and have the User role in the Plunge Development server.\n\nHead over to the Plunge Development server to see!", inline=False)
            await ctx.send(embed=embed)

        # Update the users info in the userInfo.json anyway
        userInfo[str(ctx.author.id)] = str(ctx.guild.id)

        with open('json/userInfo.json', 'w') as f:
            json.dump(userInfo, f, indent=4)
    else:
        embed=discord.Embed(title="Plunge", description=f"{ctx.author.mention}, you are not in the Plunge Development server. [Click here](https://discord.gg/mjr6nUU) to join!\n\nAfter you are in the Plunge Development server, run the `p.verify` command again to get your role.", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        await ctx.send(embed=embed)
    
# Command to join the developer discord
# p.server, p.join, p.discord
@client.command(aliases=['join', 'discord'])
async def server(ctx):
    embed=discord.Embed(title="Plunge Development", description="To join our discord, [click here](https://discord.gg/mjr6nUU) for an invite", color=0xfd5d5d)
    embed.set_thumbnail(url=logourl)
    await ctx.send(embed=embed)

# Command that leaves a suggestion for the bot
# p.suggest (suggestion)  p.feedback (feedback)
@client.command(aliases=['feedback'])
async def suggest(ctx, *, suggestion = None):
    if suggestion is None:
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Invalid Command Format", value="Try: `p.suggest (suggestion)` or `p.feedback (feedback)`", inline=False)
        await ctx.send(embed=embed)
    else:
        # On Suggestion command, ping private discord channel 733592146308890675 with the details
        channelId = client.get_channel(733592146308890675) #suggestions in Plunge Development

        # Response to user's message
        reply=discord.Embed(title="Plunge", color=0xfd5d5d)
        reply.set_thumbnail(url=logourl)
        reply.add_field(name=f"Sent", value=f"Thanks for your submission!", inline=False)
        reply.set_footer(text="p.invite • Invites this bot to your server")
        await ctx.send(embed=reply)
        
        # Suggestion added to suggestions channel
        suggested=discord.Embed(title="Plunge", description=f"Submitted by {ctx.author.name}#{ctx.author.discriminator}", color=0xfd5d5d)
        suggested.set_thumbnail(url=ctx.author.avatar_url)
        suggested.add_field(name="Suggestion / Feedback", value=suggestion, inline=False)
        await channelId.send(embed=suggested)

# Command that gives the user information about the giveaway
# p.giveaway 
@client.command()
async def giveaway(ctx):
    embed=discord.Embed(title="Plunge", color=0xfd5d5d)
    embed.set_thumbnail(url=logourl)
    embed.add_field(name="Giveaway Information", value="Giving away `3x Discord Nitro` in the Plunge Development server.\n", inline=False)
    embed.add_field(name="To Qualify", value="1. Join the [Plunge Development server](https://discord.gg/mjr6nUU) and be sure to read the server rules.\n\n2. You need the Plunge bot in a server you own or are administrator of. Use `p.invite` or invite the bot by clicking [here](https://discord.com/api/oauth2/authorize?client_id=732864657932681278&permissions=313408&scope=bot).\n\n3. In your server, run the `p.verify` command. This will give you the User role in the Plunge Development server.\n\n4. Head back over to the giveaways channel in the [Plunge Development server](https://discord.gg/mjr6nUU) and enter the giveaway.", inline=False)
    embed.add_field(name="Note", value="If the bot is removed from the server where you used `p.verify` you will lose the User role in the Plunge Development server.", inline=False)
    await ctx.send(embed=embed)

# Send the user their match summary (kills, xp, gold, items if any)
async def matchSummary(userId, guildId):
    with open('json/users.json', 'r') as f:
        data = json.load(f)
    
    usersGuild = client.get_guild(guildId)
    member = usersGuild.get_member(userId)
    goldEmoji = client.get_emoji(736439923095109723)

    placement = data[str(userId)]['matchStats'][str(guildId)]['placement']
    killsEarned = data[str(userId)]['matchStats'][str(guildId)]['killsEarned']
    goldEarned = data[str(userId)]['matchStats'][str(guildId)]['goldEarned']
    expEarned = data[str(userId)]['matchStats'][str(guildId)]['expEarned']
    
    itemsEarned = data[str(userId)]['matchStats'][str(guildId)]['itemsEarned']
    items = ''

    if len(itemsEarned) == 1:
        items = f'{len(itemsEarned)} item earned:\n'
    elif len(itemsEarned) > 1:
        items = f'{len(itemsEarned)} items earned:\n'
    
    if len(itemsEarned) > 0:
        for itemId in itemsEarned:
            item = await fetchItem(itemId)

            itemEmoji = client.get_emoji(item['emojiId'])
            itemName = item['name']

            items += f'{itemEmoji} {itemName}\n'


    ordinal = 'th'
    
    if placement % 10 == 1 and placement != 11:
        ordinal = 'st'
    elif placement % 10 == 2 and placement != 12:
        ordinal = 'nd'
    elif placement % 10 == 3 and placement != 13:
        ordinal = 'rd'

    embed=discord.Embed(title=f"{usersGuild.name}\\'s Battle Royale", color=0xfd5d5d)
    embed.set_thumbnail(url=usersGuild.icon_url)
    embed.add_field(name=f"__Match Summary__", value=f"Placement: {placement}{ordinal}\nKills: {killsEarned}\nGold: {goldEarned} {goldEmoji}\nExp Earned: {expEarned*100}\n\n{items}", inline=False)

    await member.send(embed=embed)

# Command that shows the top users on the leaderboard (Top Wins, Top Kills, Top Gold)
# p.leaderboard
@client.command()
async def leaderboard(ctx):
    with open('json/users.json', 'r') as f:
        data = json.load(f)

    userList = []

    for user in data:
        #If its not a bot and not Plunge
        if int(user) > 20 and int(user) != 732864657932681278:
            userList.append(data[user])
    
    userList.sort(reverse=True, key=goldValue)
    sortedGold = list(userList)
    topFiveGold = topUsers(sortedGold, 'gold', 5)

    userList.sort(reverse=True, key=killsValue)
    sortedKills = list(userList)
    topFiveKills = topUsers(sortedKills, 'kills', 5)

    userList.sort(reverse=True, key=winsValue)
    sortedWins = list(userList)
    topFiveWins = topUsers(sortedWins, 'wins', 5)

    #TODO: Make this message pretty and also include the index (placement) of the user that called the function
    await ctx.send(f'Wins: \n{topFiveWins}\n\nKills:\n{topFiveKills}\n\nGold:\n{topFiveGold}')

# A function that returns the top users in a string (pass in the sorted list)
def topUsers(userList, stat, total):
    # Print the top 10
    i = 0
    topUsers = ''
    while i < total:
        name = userList[i]['name']
        if stat.lower() == 'gold':
            gold = userList[i]['inventory']['gold']
            topUsers += f'{i + 1}. **{name}** Gold: {gold}\n'
        elif stat.lower() == 'kills':
            kills = userList[i]['stats']['kills']
            topUsers += f'{i + 1}. **{name}** Kills: {kills}\n'
        elif stat.lower() == 'wins':
            wins = userList[i]['stats']['wins']
            topUsers += f'{i + 1}. **{name}** Wins: {wins}\n'
        i += 1
    
    return topUsers

# A function that returns the gold value
def goldValue(user):
    return user['inventory']['gold']

# A function that returns the kills value
def killsValue(user):
    return user['stats']['kills']

# A function that returns the wins value
def winsValue(user):
    return user['stats']['wins']

# Command that opens a chest
# p.chest
@client.command()
async def chest(ctx):
    with open('json/users.json', 'r') as f:
        data = json.load(f)
    
    totalChests = data[str(ctx.author.id)]['inventory']['chests']

    if totalChests > 0:
        # Items you can get from a chest
        # Gold 3000 - 8000 (multiple of 5)
        goldInt = random.randint(600, 1601)*5
        # Weapons Uncommon 1 in 50 chance - Rare 1 in 70 chance - Epic 1 in 75 chance - Legendary
        weaponInt = random.randint(1, 1001)

        # Weapon to give (default to nothing)
        weaponId = 999

        if weaponInt == 999:
            # Give a random legendary weapon (IDs 16 - 19)
            weaponId = random.randint(16, 20)
        elif weaponInt < 701:
            # Give an uncommon weapon (IDs 4 - 7)
            weaponId = random.randint(4, 8)
        elif weaponInt > 700 and weaponInt < 901:
            # Give a rare weapon (IDs 8 - 11)
            weaponId = random.randint(8, 12)
        elif weaponInt > 900:
            # Give an epic weapon (IDs 12 - 15)
            weaponId = random.randint(12, 16)

        # Get the footer message
        chestsRemaining = f'{totalChests - 1} chests remaining'
        if chestsRemaining == 1:
            chestsRemaining = f'{totalChests - 1} chest remaining'
        
        # Get the gold message
        goldEmoji = client.get_emoji(736439923095109723)
        goldMessage = f'**Gold:** {goldInt} {goldEmoji}'

        # Get the item message
        weapon = await fetchItem(weaponId)
        weaponName = weapon['name']
        weaponEmojiId = weapon['emojiId']
        weaponEmoji = client.get_emoji(weaponEmojiId)
        weaponMessage = f'**Weapon:** {weaponName} {weaponEmoji}'

        duplicateWeaponPrice = 0
        
        data[str(ctx.author.id)]['inventory']['chests'] -= 1

        with open('json/users.json', 'w') as f:
            json.dump(data, f, indent=4)

        result = await addItem(ctx.author.id, weaponId)
        if result == True:
            # The weapon to add is duplicate
            duplicateWeaponPrice = int(weapon['price'] / 2)
            weaponMessage = f'**Weapon:** ~~{weaponName}~~ {weaponEmoji}\n``duplicate`` +{duplicateWeaponPrice} {goldEmoji}'
        
        totalGold = duplicateWeaponPrice + goldInt
        await addGold(ctx.author.id, totalGold)



        embed=discord.Embed(color=0xfd5d5d)
        embed.add_field(name="Chest Opened", value=f"{ctx.author.mention} opened a chest and found...\n\n{goldMessage}\n{weaponMessage}", inline=False)
        embed.set_footer(text=f"{chestsRemaining}")
        await ctx.send(embed=embed)
        # TODO: Decide if we want to delete this message or not
        #await msg.delete(delay=120)

    else:
        embed=discord.Embed(color=0xfd5d5d)
        embed.add_field(name="No Chests", value=f"Sorry {ctx.author.mention}, you do not have any chests to open.", inline=False)
        embed.set_footer(text=f'participate in battles to earn chests')
        msg = await ctx.send(embed=embed)
        await msg.delete(delay=120)

# p.shop
@client.command()
async def shop(ctx):
    # Open up the shop.json file
    with open('json/shop.json', 'r') as f:
        data = json.load(f)
    
    shopPages = []

    allItems = getShopItems()
    itemStrings = await getShopStrings(allItems)

    for page in data:
        shopPages.append(page)
    
    # The total amount of pages
    pages = len(shopPages)
    # The current page
    cur_page = 1

    cur_pageTMP = cur_page
    itemsToSkip = 0
    itemsCount = len(data[str(cur_page-1)]["items"])
    displayItems = f''
    pageTitle = data[str(cur_page-1)]["title"]

    while cur_pageTMP > 1:
        itemsToSkip += len(data[str(cur_pageTMP-2)]["items"])
        cur_pageTMP -= 1
    
    for item in itemStrings[itemsToSkip:itemsToSkip+itemsCount]:
        displayItems += item

    embed=discord.Embed(title="Item Shop", color=0xfd5d5d)
    # embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name=f"{pageTitle}", value=f"\nTo buy an item from the shop, do ``p.buy (number)``\n\n{displayItems}", inline=False),
    embed.set_footer(text=f"Page {cur_page}/{pages}")

    msg = await ctx.send(embed=embed)

    await msg.add_reaction("◀️")
    await msg.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1

                cur_pageTMP = cur_page
                itemsToSkip = 0
                itemsCount = len(data[str(cur_page-1)]["items"])
                displayItems = f''
                pageTitle = data[str(cur_page-1)]["title"]

                while cur_pageTMP > 1:
                    itemsToSkip += len(data[str(cur_pageTMP-2)]["items"])
                    cur_pageTMP -= 1
                
                for item in itemStrings[itemsToSkip:itemsToSkip+itemsCount]:
                    displayItems += item

                embed=discord.Embed(title="Item Shop", color=0xfd5d5d)
                # embed.set_thumbnail(url=user.avatar_url)
                embed.add_field(name=f"{pageTitle}", value=f"\nTo buy an item from the shop, do ``p.buy (number)``\n\n{displayItems}", inline=False),
                embed.set_footer(text=f"Page {cur_page}/{pages}")

                await msg.edit(embed=embed)
                await msg.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                
                cur_pageTMP = cur_page
                itemsToSkip = 0
                itemsCount = len(data[str(cur_page-1)]["items"])
                displayItems = f''
                pageTitle = data[str(cur_page-1)]["title"]

                while cur_pageTMP > 1:
                    itemsToSkip += len(data[str(cur_pageTMP-2)]["items"])
                    cur_pageTMP -= 1
                
                for item in itemStrings[itemsToSkip:itemsToSkip+itemsCount]:
                    displayItems += item

                embed=discord.Embed(title="Item Shop", color=0xfd5d5d)
                # embed.set_thumbnail(url=user.avatar_url)
                embed.add_field(name=f"{pageTitle}", value=f"\nTo buy an item from the shop, do ``p.buy (number)``\n\n{displayItems}", inline=False),
                embed.set_footer(text=f"Page {cur_page}/{pages}")

                await msg.edit(embed=embed)

                await msg.remove_reaction(reaction, user)

            else:
                await msg.remove_reaction(reaction, user)
                # removes reactions if the user tries to go forward on the last page or
                # backwards on the first page
        except asyncio.TimeoutError:
            await msg.delete()
            break
            # ending the loop if user doesn't react after x seconds

def getShopItems():
    with open('json/shop.json', 'r') as f:
        data = json.load(f)

    allItems = []

    for i in data:
        for item in data[i]['items']:
            allItems.append(item)
    
    return allItems

async def getShopStrings(items):
    shopStrings = []
    i = 1
    for item in items:
        myItem = await fetchItem(item)

        itemPrice = myItem['price']
        goldEmoji = client.get_emoji(736439923095109723)

        itemEmojiId = myItem['emojiId']
        itemEmoji = client.get_emoji(itemEmojiId)

        itemName = myItem['name']

        if item < 1000:
            weapon = fetchWeapon(item)
            shopStrings.append(f'**{i}**: {weapon} | {itemPrice} {goldEmoji}\n')
        else:
            shopStrings.append(f'**{i}**: {itemEmoji} {itemName} | {itemPrice} {goldEmoji}\n')
        
        i += 1

        # emojiId = myItem['emojiId']
        # emoji = client.get_emoji(emojiId)
        # itemName = myItem['name']


        # shopString += f'**{i}**: {emoji} {itemName}'
    return shopStrings

######### ITEMS/SHOP ITEMS ##########
#  TIERS: Common - 0, Uncommon - 1, Rare - 2, Epic - 3, Legendary - 4, POSSIBLY MYTHIC - 5 (NOT RELEASED)
#  
#  Weapon Categories: Shotgun, Smg, Ar, Sniper
#
#  Perks: Extra gold at end of game, Extra Threat for the game, Extra Experience per game


# Command that buys you the weapon from the shop
# p.buy number
@client.command()
async def buy(ctx, number = None):
    if number == None:
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Invalid Command Format", value="Please provide a number that correlates to the item in the shop that you want to buy. \nExample: `p.buy 5`", inline=False)
        await ctx.send(embed=embed)
    else:
        try:
        
            user = await fetchUserProfile(ctx.author.id)
            usersGold = user['inventory']['gold']
            usersInventory = user['inventory']['weapons'] + user['inventory']['perks'] + user['inventory']['umbrellas'] + user['inventory']['titles'] + user['inventory']['pickaxes']

            allShopItems = getShopItems()
            itemToGrab = int(number) - 1

            if itemToGrab >= len(allShopItems):
                # Don't purchase the item
                embed=discord.Embed(color=0xfd5d5d)
                embed.add_field(name="**Purchase Failed**", value=f"Make sure you are entering the correct number from the shop.", inline=False)
                failed = await ctx.send(embed=embed)
                await failed.delete(delay=60)
            else:
                itemToBuy = allShopItems[itemToGrab]

                item = await fetchItem(itemToBuy)

                itemName = item['name']
                itemEmojiId = item['emojiId']
                itemEmoji = client.get_emoji(itemEmojiId)
                itemPrice = item['price']
                goldEmoji = client.get_emoji(736439923095109723)
                

                # If user has the item...
                if itemToBuy in usersInventory:
                    # Don't purchase the item
                    embed=discord.Embed(color=0xfd5d5d)
                    embed.add_field(name="**Purchase Failed**", value=f"You already own the item you are trying to buy.", inline=False)
                    failed = await ctx.send(embed=embed)
                    await failed.delete(delay=60)
                # If user doesn't have enough gold
                elif usersGold < itemPrice:
                    # Dont purchase the item
                    embed=discord.Embed(color=0xfd5d5d)
                    embed.add_field(name="**Purchase Failed**", value=f"You do not have enough gold to buy the item.", inline=False)
                    failed = await ctx.send(embed=embed)
                    await failed.delete(delay=60)
                else:
                    # Buy the item
                    await removeGold(ctx.author.id, itemPrice)
                    await addItem(ctx.author.id, itemToBuy)
                    embed=discord.Embed(color=0xfd5d5d)
                    embed.add_field(name="**Purchase Complete**", value=f"**Weapon:** {itemName} {itemEmoji}\n**Gold:** -{itemPrice} {goldEmoji}", inline=False)
                    complete = await ctx.send(embed=embed)
                    await complete.delete(delay=60)
        except:
            # Don't purchase the item
            embed=discord.Embed(color=0xfd5d5d)
            embed.add_field(name="**Purchase Failed**", value=f"Make sure you are entering the correct number from the shop.", inline=False)
            failed = await ctx.send(embed=embed)
            await failed.delete(delay=60)

# Command that lets you equip an item from your inventory
# p.equip [id]

# Command that lets you unequip a certain item from your loadout or all items
# p.unequip [id/all]

# Command that equips the showcase items

# Command that removes the showcase items



####################
# Start Battle commands
####################

# Battle function
async def battleStart(ctx, users):

    # weapons = ['a Pistol', 'a Pickaxe', 'an Assault Rifle', 'an Auto Rifle', 'a Sniper Rifle', 'a Paintball Gun', 'a Rock', 'an Arrow', 'a Blow Dart Gun', 'a Rocket Launcher', 
    # 'a Grenade', 'a Grenade Launcher', 'a Shotgun', 'Hand to Hand Combat', 'a Submachine Gun', 'a Light Machine Gun', 'a Stick', 'an Eye Poke', 'a Karate Chop']

    # eliminations = ['eliminated', 'destroyed', 'annihilated', 'obliterated', 'got rid of', 'beamed', 'ended', 'finished off', 'murdered', 'killed', 'erased']

    funny = ['took an arrow to the knee', 'forgot they can\'t fly', 'starved to death', 'was eliminated for cheating', 
    'went off the deep end', 'drowned', 'fell', 'died', 'mysteriously disappeared', 'fled from battle', 'was pecked to death by a bird',
    'sunk in quick sand', 'was trampled by rhinos', 'died from the unknown', 'fell in the void', 'got a deadly infection', 'was squashed',
    'was poisoned', 'choked on a raisin', 'didn\'t make it', 'hyperventilated and died', 'was eliminated for tax evasion']

    # Adds to the battle counter
    await addBattle()

    # Checks the users in the list... removes Plunge Bot
    for userId in list(users):
        await createNewUser(userId)
        await addMatchStats(userId, ctx.guild.id)

    # TODO: Fix whatever mess this is
    newList = users
    totalPlayers = len(list(newList))
    PlayersForXp = list(newList)
    
    while len(newList) > 1:
        with open('json/users.json', 'r') as f:
            data = json.load(f)

        userId1 = random.choice(users)
        userId2 = random.choice(users)

        battleRange = random.randint(1, 151)

        chestNumber = random.randint(1, 501)

        if chestNumber == 499:
            allPlayers = []

            # Gives an actual player a chest
            for user in newList:
                if user > 20:
                    allPlayers.append(user)

            if len(allPlayers) != 0:
                chestWinner = random.choice(allPlayers)
                
                chestUser = client.get_user(chestWinner)
                if chestUser is not None:
                    chestUserName = f'{chestUser.mention}'
                else:
                    print('something went wrong [addChest(chestWinner, ctx.guild.id)]')
                    chestUserName = data[str(chestWinner)]['name']

                addChest(chestWinner, ctx.guild.id)

                # TODO: Add chest emoji
                embed=discord.Embed(color=0xfd5d5d)
                embed.add_field(name="Chest Found", value=f"{chestUserName} found a chest!", inline=False)
                embed.set_footer(text=f"use p.chest to open it")
                msg = await ctx.send(embed=embed)
                await msg.delete(delay=120)


        await asyncio.sleep(random.randint(4,8)) # Randomly select the message delay between 4-8 numbers

        # Prevents them from randomly dying without getting eleminated when its in the final 5
        if len(newList) <= 5:
            i = 0
            while i < 3 and userId1 == userId2:
                userId1 = random.choice(newList)
                userId2 = random.choice(newList)
                i+=1

        if userId1 == userId2:

            if userId1 > 20:
                user1 = client.get_user(userId1)
                if user1 is not None:
                    user1Name = f'{user1.mention}'
                else:
                    print('but something went wrong 1260')
                    user1Name = data[str(userId1)]['name']
            else:
                user1Name = data[str(userId1)]['name']

            await addDeath(userId1, ctx.guild.id, len(newList))
            embed=discord.Embed()
            embed.add_field(name="Elimination", value=f'**{user1Name}** {random.choice(funny)}', inline=False)
            embed.set_footer(text=f"{len(newList) - 1} Remaining")
            msg = await ctx.send(embed=embed)
            await msg.delete(delay=120)

            # Updates the list by removing the user that got eliminated
            newList.remove(userId2)
        else:
            # Call the method that calculates who wins the battle (returns the elimination message)
            elimMessage = userBattle(userId1, userId2, battleRange)
            addKill(elimMessage[1], ctx.guild.id)
            await addDeath(elimMessage[2], ctx.guild.id, len(newList))
            embed=discord.Embed()
            embed.add_field(name="Elimination", value=f'{elimMessage[0]}', inline=False)
            embed.set_footer(text=f"{len(newList) - 1} Remaining")
            msg = await ctx.send(embed=embed)
            await msg.delete(delay=120)
            
            # Updates the list by removing the user that got eliminated
            newList.remove(elimMessage[2])

    await asyncio.sleep(3)

    winner = newList[0]

    await addWin(winner, ctx.guild.id)

    # Get the winners name
    if winner > 20:
        winnerUser = client.get_user(winner)
        winnerName = f'{winnerUser.mention}'
    else:
        winnerName = data[str(winner)]['name']
    
    winnerKills = getGameKills(winner, ctx.guild.id)

    #TODO: Put crown for thumbnail url in embed message. add other emojis for victory

    embed=discord.Embed(title="Battle Royale Victory", description=f"The winner of {ctx.guild.name}\'s Battle Royale is **{winnerName}**\n\n**{winnerName}** had {winnerKills} kills", color=0xfd5d5d)
    embed.set_thumbnail(url=logourl)
    embed.set_footer(text=f"{totalPlayers} players participated")
    await ctx.send(embed=embed)

    for userId in PlayersForXp:
        await resetMatchStats(userId, ctx.guild.id)

def userBattle(userId1, userId2, battleRange):
    with open('json/users.json', 'r') as f:
        users = json.load(f)
    
    with open('json/ranges.json', 'r') as f:
        ranges = json.load(f)

    eliminations = ['eliminated', 'destroyed', 'annihilated', 'obliterated', 'got rid of', 'beamed', 'ended', 'finished off', 'murdered', 'killed', 'erased']

    # Get user1's weapon loadout
    user1Loadout = []
    user1Loadout.append(users[str(userId1)]['loadout']['slot1'])
    user1Loadout.append(users[str(userId1)]['loadout']['slot2'])
    user1Loadout.append(users[str(userId1)]['loadout']['slot3'])
    user1Loadout.append(users[str(userId1)]['loadout']['slot4'])

    # Get desired weapon for user 1
    user1Weapon = desiredWeapon(user1Loadout, battleRange)

    # Get weapon emoji
    user1WeaponEmojiId = user1Weapon['emojiId']
    user1WeaponEmoji = client.get_emoji(user1WeaponEmojiId)

    # Get weapon name
    user1WeaponName = user1Weapon['name']

    # Get user1's weapon ranges
    user1MinRange = ranges[str(user1Weapon['rangeId'])]['minRange']
    user1MaxRange = ranges[str(user1Weapon['rangeId'])]['maxRange']
    user1RangeBonusThreat = 0

    # Get user1's bonus threat if any
    if battleRange <= user1MaxRange and battleRange >= user1MinRange:
        user1RangeBonusThreat = ranges[str(user1Weapon['rangeId'])]['bonusThreat']

    # Get user1's loadout threat
    user1LoadoutThreat = getUsersThreat(users[str(userId1)])

    # Get user2's weapon loadout
    user2Loadout = []
    user2Loadout.append(users[str(userId2)]['loadout']['slot1'])
    user2Loadout.append(users[str(userId2)]['loadout']['slot2'])
    user2Loadout.append(users[str(userId2)]['loadout']['slot3'])
    user2Loadout.append(users[str(userId2)]['loadout']['slot4'])

    # Get desired weapon for user 2
    user2Weapon = desiredWeapon(user2Loadout, battleRange)

    # Get weapon emoji
    user2WeaponEmojiId = user2Weapon['emojiId']
    user2WeaponEmoji = client.get_emoji(user2WeaponEmojiId)

    # Get weapon name
    user2WeaponName = user2Weapon['name']

    # Get user2's weapon ranges
    user2MinRange = ranges[str(user2Weapon['rangeId'])]['minRange']
    user2MaxRange = ranges[str(user2Weapon['rangeId'])]['maxRange']
    user2RangeBonusThreat = 0

    # Get user2's bonus threat if any
    if battleRange <= user2MaxRange and battleRange >= user2MinRange:
        user2RangeBonusThreat = ranges[str(user2Weapon['rangeId'])]['bonusThreat']

    # Get user2's ladout threat
    user2LoadoutThreat = getUsersThreat(users[str(userId2)])

    # Get user2's total threat
    user2TotalThreat = user2RangeBonusThreat + user2LoadoutThreat

    # Get user1's total threat
    user1TotalThreat = user1RangeBonusThreat + user1LoadoutThreat

    # Get the odds per user TODO: Maybe change the odds again
    if user1TotalThreat > user2TotalThreat:
        difference = user1TotalThreat - user2TotalThreat
        user1odds = (70 + difference) / 2
        user2odds = (70 - difference) / 2
    elif user1TotalThreat == user2TotalThreat:
        user1odds = 50
        user2odds = 50
    else:
        difference = user2TotalThreat - user1TotalThreat
        user2odds = (70 + difference) / 2
        user1odds = (70 - difference) / 2

    weightedList = [userId1, userId2]

    winningId = random.choices(weightedList, weights=(user1odds, user2odds))

    # Use pickaxes if the battle range is 1
    if battleRange == 1:
        with open('json/pickaxes.json', 'r') as f:
            pickaxes = json.load(f)

        user1PickaxeId = users[str(userId1)]['loadout']['pickaxe']
        user1PickaxeEmojiId = pickaxes[str(user1PickaxeId)]['emojiId']
        user1PickaxeName = pickaxes[str(user1PickaxeId)]['name']

        user1WeaponEmoji = client.get_emoji(user1PickaxeEmojiId)
        user1WeaponName = user1PickaxeName

        user2PickaxeId = users[str(userId2)]['loadout']['pickaxe']
        user2PickaxeEmojiId = pickaxes[str(user2PickaxeId)]['emojiId']
        user2PickaxeName = pickaxes[str(user2PickaxeId)]['name']

        user2WeaponEmoji = client.get_emoji(user2PickaxeEmojiId)
        user2WeaponName = user2PickaxeName
    
    # Fetch the users names to use
    if userId1 > 20:
        user1 = client.get_user(userId1)
        user1Name = f'{user1.mention}'
    else:
        user1Name = users[str(userId1)]['name']

    if userId2 > 20:
        user2 = client.get_user(userId2)
        user2Name = f'{user2.mention}'
    else:
        user2Name = users[str(userId2)]['name']

    if winningId[0] == userId1:
        # User1 wins
        return f'**{user1Name}** {random.choice(eliminations)} **{user2Name}** with {user1WeaponEmoji} {user1WeaponName} (*{battleRange}m*)', userId1, userId2
    else:
        # User2 wins
        return f'**{user2Name}** {random.choice(eliminations)} **{user1Name}** with {user2WeaponEmoji} {user2WeaponName} (*{battleRange}m*)', userId2, userId1

# Gets a users total threat
def getUsersThreat(user):
    with open('json/weapons.json', 'r') as f:
        weapons = json.load(f)
    
    with open('json/rarity.json', 'r') as f:
        rarity = json.load(f)

    totalThreat = 0

    # Get users loadout
    userLoadout = []
    userLoadout.append(user['loadout']['slot1'])
    userLoadout.append(user['loadout']['slot2'])
    userLoadout.append(user['loadout']['slot3'])
    userLoadout.append(user['loadout']['slot4'])

    for weaponId in userLoadout:
        totalThreat += rarity[str(weapons[str(weaponId)]['rarityId'])]['threat']
    
    if user['loadout']['perk'] == 1000:
        totalThreat += 2

    return totalThreat

# Gets the desired weapon for the user to use for the engagement
def desiredWeapon(weaponIdList, battleRange):
    with open('json/weapons.json', 'r') as f:
        weapons = json.load(f)

    with open('json/ranges.json', 'r') as f:
        ranges = json.load(f)

    # average list
    averageRanges = []

    # get the average of the ranges and add them to the list
    for weaponId in weaponIdList:
        if weaponId != 999:
            rangeId = weapons[str(weaponId)]['rangeId']

            averageRange = ranges[str(rangeId)]['averageRange']

            averageRanges.append(averageRange)

    if (averageRanges != []):   
        # weaponRange to use
        rangeToUse = closest(averageRanges, battleRange)

        for weaponId in weaponIdList:
            rangeId = weapons[str(weaponId)]['rangeId']
            
            if rangeToUse == ranges[str(rangeId)]['averageRange']:
                return weapons[str(weaponId)]
    else:
        # Use a stone as a weapon TODO: Update the stone emoji in weapons.json
        return weapons["998"]


def closest(lst, distance):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-distance))]

# Method that gets the current Game Kills
def getGameKills(userId, serverId):
    with open('json/users.json', 'r') as f:
        data = json.load(f)

    kills = data[str(userId)]['matchStats'][str(serverId)]['killsEarned']

    return kills

# Method that updates your stats at the end of the game
async def resetMatchStats(userId, serverId):
    with open('json/users.json', 'r') as f:
        data = json.load(f)

    data[str(userId)]['matchStats'][str(serverId)]['placement'] = 0
    data[str(userId)]['matchStats'][str(serverId)]['killsEarned'] = 0
    data[str(userId)]['matchStats'][str(serverId)]['goldEarned'] = 0
    data[str(userId)]['matchStats'][str(serverId)]['expEarned'] = 0
    data[str(userId)]['matchStats'][str(serverId)]['itemsEarned'] = []

    with open('json/users.json', 'w') as f:
        json.dump(data, f, indent=4)

# Method that adds a chest to the user
def addChest(userId, serverId):
    with open('json/users.json', 'r') as f:
        data = json.load(f)

    data[str(userId)]['inventory']['chests'] += 1
    data[str(userId)]['matchStats'][str(serverId)]['itemsEarned'].append(4000)

    with open('json/users.json', 'w') as f:
        json.dump(data, f, indent=4)

# Method that updates the users kills
def addKill(userId, serverId):
    with open('json/users.json', 'r') as f:
        data = json.load(f)

    goldToAdd = 10
    expToAdd = 1

    if data[str(userId)]['loadout']['perk'] == 1001:
        goldToAdd = int(round((10 * .1) + 10))
    elif data[str(userId)]['loadout']['perk'] == 1002:
        expToAdd = int(round((1 * .1) + 1))

    data[str(userId)]['stats']['kills'] += 1
    data[str(userId)]['matchStats'][str(serverId)]['killsEarned'] += 1
    data[str(userId)]['stats']['totalExp'] += expToAdd
    data[str(userId)]['matchStats'][str(serverId)]['expEarned'] += expToAdd
    data[str(userId)]['inventory']['gold'] += goldToAdd
    data[str(userId)]['matchStats'][str(serverId)]['goldEarned'] += goldToAdd

    with open('json/users.json', 'w') as f:
        json.dump(data, f, indent=4)

# Method that updates the users wins
async def addWin(userId, serverId):
    with open('json/users.json', 'r') as f:
        data = json.load(f)

    goldToAdd = 150
    expToAdd = 10

    if data[str(userId)]['loadout']['perk'] == 1001:
        goldToAdd = int(round((150 * .1) + 150))
    elif data[str(userId)]['loadout']['perk'] == 1002:
        expToAdd = int(round((10 * .1) + 10))

    data[str(userId)]['stats']['wins'] += 1
    data[str(userId)]['matchStats'][str(serverId)]['placement'] = 1
    data[str(userId)]['stats']['totalExp'] += expToAdd
    data[str(userId)]['matchStats'][str(serverId)]['expEarned'] += expToAdd
    data[str(userId)]['inventory']['gold'] += goldToAdd
    data[str(userId)]['matchStats'][str(serverId)]['goldEarned'] += goldToAdd
    
    if 2001 not in data[str(userId)]['inventory']['umbrellas']:
        data[str(userId)]['matchStats'][str(serverId)]['itemsEarned'].append(2001)
        data[str(userId)]['inventory']['umbrellas'].append(2001)

    with open('json/users.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    if userId > 20:
        await matchSummary(userId, serverId)

# Method that updates the users deaths
async def addDeath(userId, serverId, placement):
    with open('json/users.json', 'r') as f:
        data = json.load(f)

    goldToAdd = 50
    expToAdd = 5

    if data[str(userId)]['loadout']['perk'] == 1001:
        goldToAdd = int(round((50 * .1) + 50))
    elif data[str(userId)]['loadout']['perk'] == 1002:
        expToAdd = int(round((5 * .1) + 5))

    data[str(userId)]['matchStats'][str(serverId)]['placement'] = placement
    data[str(userId)]['stats']['deaths'] += 1
    data[str(userId)]['stats']['totalExp'] += expToAdd
    data[str(userId)]['matchStats'][str(serverId)]['expEarned'] += expToAdd
    data[str(userId)]['inventory']['gold'] += goldToAdd
    data[str(userId)]['matchStats'][str(serverId)]['goldEarned'] += goldToAdd
        

    with open('json/users.json', 'w') as f:
        json.dump(data, f, indent=4)

    if userId > 20:
        await matchSummary(userId, serverId)

####################
# End Battle commands
####################

####################
# Start Error Handling
####################

# Command Not Found Error Handler
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Command Not Found", value="Try `p.help` for a list of all commands.", inline=False)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        pass
    else:
        raise error

# On verify command error
@verify.error
async def verify_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Missing Permissions", value="To verify for the User role in the Plunge Development server, you need to be an administrator or have permissions to manage the server you are currently in.", inline=False)
        embed.add_field(name="To Verify", value="[Invite the bot](https://discord.com/api/oauth2/authorize?client_id=732864657932681278&permissions=313408&scope=bot) to a server you own or are administrator of and use `p.verify` there.", inline=False)
        await ctx.send(embed=embed)

####################
# End Error Handling
####################

# Runs the bot
client.run(data['token'])