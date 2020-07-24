import discord
from discord.ext import commands, tasks
import random
import math
import json
import asyncio

# The prefix for all the commands
prefix = "p."
activeBattles = []
activeUsers = []
client = commands.Bot(command_prefix = prefix, case_insensitive=True)
client.remove_command('help')

# The url for our logo
logourl = "https://i.imgur.com/tdbgl13.png"

# Reads the Auth.json File
with open('auth.json', 'r') as f:
    data = json.load(f)

# Updates and cycles the bots status
async def change_status():
    while True:
        await client.change_presence(
            activity=discord.Game('Dropped ' + str(getInfo('drops')) + " times!")
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
            activity=discord.Game(' p.help • p.verify • p.invite')
        )

        await asyncio.sleep(15)

        await client.change_presence(
            activity=discord.Game('Hosted ' + str(getInfo('battles')) + " battles!")
        )

        await asyncio.sleep(15)

        await client.change_presence(
            activity=discord.Game(' p.drop • p.battle • p.stats')
        )

        await asyncio.sleep(15)

# Displays that the bot is ready
@client.event
async def on_ready():
    #change_status.start()
    client.loop.create_task(change_status())
    print('Bot is ready.')

# Gets the amount of drops
def getInfo(info):
    with open('info.json', 'r') as f:
        drops = json.load(f)
    
    return drops[info]

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
    elif isinstance(error, commands.MissingPermissions):
        pass
    else:
        raise error


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

# Help Command
# p.help
@client.command()
async def help(ctx, setting = None):
    if setting is None:
        embed=discord.Embed(title="Plunge", description="List of Commands", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="General", value=f"`{prefix}drop` `{prefix}battle` `{prefix}help` `{prefix}feedback` `{prefix}invite` `{prefix}discord` `{prefix}verify` `{prefix}giveaway`", inline=False)
        embed.add_field(name="Info", value=f"To get more help on a command or see the command's function, try: `p.help (command)`", inline=False)
        await ctx.send(embed=embed)
    elif setting.lower() == "drop":
        embed=discord.Embed(title="Plunge", description="Drop Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Gives you a random location to drop in Fortnite!", inline=False)
        embed.add_field(name="Usage:", value="`p.drop`", inline=False)
        await ctx.send(embed=embed)
    elif setting.lower() == "battle":
        embed=discord.Embed(title="Plunge", description="Battle Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Starts a simulated battle royale for your server.", inline=False)
        embed.add_field(name="Usage:", value="`p.battle`", inline=False)
        embed.set_footer(text="p.stats • view your battle royale stats")
        await ctx.send(embed=embed)
    elif setting.lower() == "suggest":
        embed=discord.Embed(title="Plunge", description="Suggest Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Sends your suggestion to the developers to review.", inline=False)
        embed.add_field(name="Usage:", value="`p.suggest (your suggestion)`", inline=False)
        await ctx.send(embed=embed)
    elif setting.lower() == "feedback":
        embed=discord.Embed(title="Plunge", description="Feedback Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Sends your feedback for the developers to review.", inline=False)
        embed.add_field(name="Usage:", value="`p.feedback (your feedback)`", inline=False)
        await ctx.send(embed=embed)
    elif setting.lower() == "invite":
        embed=discord.Embed(title="Plunge", description="Invite Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Gives you a link to invite this bot to your server!", inline=False)
        embed.add_field(name="Usage:", value="`p.invite`", inline=False)
        await ctx.send(embed=embed)
    elif setting.lower() == "discord":
        embed=discord.Embed(title="Plunge", description="Discord Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Invites you to the bot's development server!", inline=False)
        embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
        embed.add_field(name="Aliases:", value="`p.server`, `p.join`, `p.support`", inline=False)
        await ctx.send(embed=embed)
    elif setting.lower() == "server":
        embed=discord.Embed(title="Plunge", description="Server Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Invites you to the bot's development server!", inline=False)
        embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
        embed.add_field(name="Aliases:", value="`p.discord`, `p.join`, `p.support`", inline=False)
        await ctx.send(embed=embed)
    elif setting.lower() == "join":
        embed=discord.Embed(title="Plunge", description="Join Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Invites you to the bot's development server!", inline=False)
        embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
        embed.add_field(name="Aliases:", value="`p.discord`, `p.server`, `p.support`", inline=False)
        await ctx.send(embed=embed)
    elif setting.lower() == "support":
        embed=discord.Embed(title="Plunge", description="Support Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Invites you to the bot's development server!", inline=False)
        embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
        embed.add_field(name="Aliases:", value="`p.discord`, `p.server`, `p.join`", inline=False)
        await ctx.send(embed=embed)
    elif setting.lower() == "verify":
        embed=discord.Embed(title="Plunge", description="Verify Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Verifies that you have the bot in your server, giving you the User Role in the Plunge Development server.", inline=False)
        embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
        await ctx.send(embed=embed)
    elif setting.lower() == "giveaway":
        embed=discord.Embed(title="Plunge", description="Giveaway Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Displays information about the current giveaway.", inline=False)
        embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Plunge", description="Invalid Command Setting", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Try:", value=f"`p.help` or `p.help (command)`", inline=False)
        await ctx.send(embed=embed)

        
# Command to let the user know where to drop using the drop command
# Can't decide on where to drop in Fortnite? It happens to us all, we  are riding in the battle bus with our maps open but no location marked.  
# Before we know it, we are getting kicked off the bus with little to no options to land. Luckily, Plunge Bot can help. With a simple command 
# "p.drop", Plunge will randomly select a location for you to drop in Fortnite, making your next drop stress free.
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



    # locationurl = f'http://www.genplus.xyz/plunge/images/{location.replace(" ", "%20")}.png'
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
    await ctx.send(embed=embed)


    #####################################################################
    #####################################################################
    ##                                                                 ##
    ##                      Server Commands                            ##
    ##                                                                 ##
    #####################################################################
    #####################################################################

@client.command()
async def updates(ctx):
    if isDev(ctx):
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

    #####################################################################
    #####################################################################


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
async def servers(ctx):
    embed=discord.Embed(title="Plunge", color=0xfd5d5d)
    embed.set_thumbnail(url=logourl)
    embed.add_field(name="Plunge is in:", value=f"{str(len(client.guilds))} servers", inline=False)
    for guild in client.guilds:
        print(guild.name)
    await ctx.send(embed=embed)

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

        with open('userInfo.json', 'r') as f:
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

        with open('userInfo.json', 'w') as f:
            json.dump(userInfo, f, indent=4)
    else:
        embed=discord.Embed(title="Plunge", description=f"{ctx.author.mention}, you are not in the Plunge Development server. [Click here](https://discord.gg/mjr6nUU) to join!\n\nAfter you are in the Plunge Development server, run the `p.verify` command again to get your role.", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        await ctx.send(embed=embed)

@verify.error
async def verify_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Missing Permissions", value="To verify for the User role in the Plunge Development server, you need to be an administrator or have permissions to manage the server you are currently in.", inline=False)
        embed.add_field(name="To Verify", value="[Invite the bot](https://discord.com/api/oauth2/authorize?client_id=732864657932681278&permissions=313408&scope=bot) to a server you own or are administrator of and use `p.verify` there.", inline=False)
        await ctx.send(embed=embed)

# On guild removed, it removes the users role in Plunge development and removes them from the userInfo.json and sends the users effected a dm.
@client.event
async def on_guild_remove(guild):
    ourGuild = client.get_guild(733551377611096195)

    with open('userInfo.json', 'r') as f:
        userInfo = json.load(f)

    for key, value in list(userInfo.items()):
        if (value == str(guild.id)):
            userInfo.pop(key)

            with open('userInfo.json', 'w') as f:
                json.dump(userInfo, f, indent=4)

            await ourGuild.get_member(int(key)).remove_roles(ourGuild.get_role(733559654210207885), reason="They removed the bot from their server.")
            await ourGuild.get_member(int(key)).add_roles(ourGuild.get_role(733558248401272832), reason="They removed the bot from their server.")

            embed=discord.Embed(title="Plunge", color=0xfd5d5d)
            embed.set_thumbnail(url=logourl)
            embed.add_field(name="Verification Revoked", value="Hey, looks like you are no longer verified. The bot is no longer in the server you were verified in. Unfortunately, you have lost the User role in the Plunge Development server.\n\nYou can [invite the bot](https://discord.com/api/oauth2/authorize?client_id=732864657932681278&permissions=313408&scope=bot) to another server and use the `p.verify` command to get back the User role.", inline=False)

            await ourGuild.get_member(int(key)).send(embed=embed)
    
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

#####################################################################
#####################################################################
##                                                                 ##
##                      Battle Royale                              ##
##                                                                 ##
#####################################################################
#####################################################################

#JSON TODO: 
# Perks     (ID's range from 1000 - 1999) (Threat Boost, Gold Boost, Experience Boost) DONE
# Umbrellas (ID's range from 2000 - 2999) (Beta Umbrealla, Umbrella) DONE
# Titles    (ID's range from 3000 - 3999) (Staff, Mod, 2020 Nitro Champ, Beta Tester) DONE
# Chests   (ID's range from 4000 - 4999) (Rare Chest, Epic Chest, Legendary Chest) DONE
# Pickaxes  (ID's range from 5000 - 5999) (Default) DONE

# NEED ATLEAST 20 Players to start
# TODO: IF user is in a battle, don't start battle
# TODO: React if you want to battle as: A group (No Rewards earned or stats counted) OR with Bots (Rewards + Stats counted)
# TODO: Add Crate Rewards (Crates have rarity)

# TODO: Add Perk Slot (+threat, +gold, +xp)

# TODO: Randomly Find Crates in games 1 in 200 chance

# TODO: Match summary (kills, xp, gold, items if any)
# TODO: Add a currency system (Gold and Gems)


# TODO: Add distance before the battle engagement to determine which weapons will get a boost


# Gets weapon Range value in a list
    # l = range(20,30)
    # z = []
    # for i in l:
    #     z.append(i)
    # print(z)

# TODO: Add a shop with items
######### ITEMS/SHOP ITEMS ##########
#  TIERS: Common - 0, Uncommon - 1, Rare - 2, Epic - 3, Legendary - 4, POSSIBLY MYTHIC - 5 (NOT RELEASED)
#  
#  Weapon Categories: Shotgun, Smg, Ar, Sniper
#
#  Perks: Extra gold at end of game, Extra Threat for the game, Extra Experience per game
#
# TODO: Add special Umbrella when you win

# Command that simulates a battle royale
# p.battle
@client.command()
async def battle(ctx):
    emoji = client.get_emoji(734656507194507275)

    # If the guild has an active battle royale... tell them.... Else start a battle royale
    if ctx.guild.id in list(activeBattles):
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle In Progress", value="There is a battle in progress, please wait until the current battle is complete", inline=False)
        await ctx.send(embed=embed)
    else:
        # add the guild to the active battles check
        activeBattles.append(ctx.guild.id)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value=f"React to the message below with {emoji} to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 30 seconds!", inline=False)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('<:plunge:734656507194507275>')

        await asyncio.sleep(10)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value=f"React to the message below with {emoji} to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 20 seconds!", inline=False)
        await msg.edit(embed=embed)

        await asyncio.sleep(10)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value=f"React to the message below with {emoji} to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 10 seconds!", inline=False)
        await msg.edit(embed=embed)

        await asyncio.sleep(5)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value=f"React to the message below with {emoji} to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 5 seconds!", inline=False)
        await msg.edit(embed=embed)

        await asyncio.sleep(1)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value=f"React to the message below with {emoji} to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 4 seconds!", inline=False)
        await msg.edit(embed=embed)

        await asyncio.sleep(1)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value=f"React to the message below with {emoji} to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 3 seconds!", inline=False)
        await msg.edit(embed=embed)

        await asyncio.sleep(1)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value=f"React to the message below with {emoji} to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 2 seconds!", inline=False)
        await msg.edit(embed=embed)

        await asyncio.sleep(1)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value=f"React to the message below with {emoji} to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 1 seconds!", inline=False)
        await msg.edit(embed=embed)

        await asyncio.sleep(1)

        # Caches your message so you can get the reactions
        cache_msg = discord.utils.get(client.cached_messages, id = msg.id)
        
        # loops through the reactions
        for reaction in cache_msg.reactions:
            # if reaction is the plunge emoji...
            if str(reaction.emoji) == '<:plunge:734656507194507275>':
                # Grabs the users that used that reaction
                users = await reaction.users().flatten()

                # If the list is larger than or equal to 5 TODO: Change the minimum players back (Decide on minimum players)
                if len(users) > 1:
                    await msg.delete(delay=None)
                    embed=discord.Embed(title="Plunge", color=0xfd5d5d)
                    embed.set_thumbnail(url=logourl)
                    embed.add_field(name="Battle In Progress...", value="Good Luck Everyone!", inline=False)
                    embed.set_footer(text=f"{len(users) - 1} Players Entered")
                    await ctx.send(embed=embed)

                    # Pass the ctx and users list into the battleStart function
                    await battleStart(ctx, users)
                else:
                    await msg.delete(delay=None)
                    embed=discord.Embed(title="Plunge", color=0xfd5d5d)
                    embed.set_thumbnail(url=logourl)
                    embed.add_field(name="Battle Cancelled", value="Sorrry, you need a minimum of 5 players to begin a Battle Royale.", inline=False)
                    await ctx.send(embed=embed)
                
        # removes the guild from the active battles check (this comes last)
        activeBattles.remove(ctx.guild.id)

# Battle function
async def battleStart(ctx, users):
    # TODO: More custom messages... more related to fortnite I guess...

    weapons = ['a Pistol', 'a Pickaxe', 'an Assault Rifle', 'an Auto Rifle', 'a Sniper Rifle', 'a Paintball Gun', 'a Rock', 'an Arrow', 'a Blow Dart Gun', 'a Rocket Launcher', 
    'a Grenade', 'a Grenade Launcher', 'a Shotgun', 'Hand to Hand Combat', 'a Submachine Gun', 'a Light Machine Gun', 'a Stick', 'an Eye Poke', 'a Karate Chop']

    eliminations = ['eliminated', 'destroyed', 'annihilated', 'obliterated', 'got rid of', 'beamed', 'ended', 'finished off', 'murdered', 'killed', 'erased']

    funny = ['took an arrow to the knee', 'forgot they can\'t fly', 'starved to death', 'was eliminated for cheating', 
    'went off the deep end', 'drowned', 'fell', 'died', 'mysteriously disappeared', 'fled from battle', 'was pecked to death by a bird',
    'sunk in quick sand', 'was trampled by rhinos', 'died from the unknown', 'fell in the void', 'got a deadly infection', 'was squashed',
    'was poisoned', 'choked on a raisin', 'didn\'t make it', 'hyperventilated and died', 'was eliminated for tax evasion']

    with open('info.json', 'r') as info:
        battles = json.load(info)
    
    battles["battles"] += 1

    with open('info.json', 'w') as info:
        json.dump(battles, info, indent=4)

    # Checks the users in the list... removes Plunge Bot
    for user in list(users):
        if user.id == 732864657932681278:
            users.remove(user)
        else:
            await newUser(ctx, user)

    newList = users
    

    totalPlayers = len(list(newList))
    PlayersForXp = list(newList)
    
    while len(newList) > 1:
        user1 = random.choice(users)
        user2 = random.choice(users)

        await asyncio.sleep(random.randint(4,8)) # Randomly select the message delay between 4-8 numbers

        # TODO: Send users a custom messages based on their placement??

        # Prevents them from randomly dying without getting eleminated when its in the final 5
        if len(newList) <= 5:
            i = 0
            while i < 3 and user1 == user2:
                user1 = random.choice(newList)
                user2 = random.choice(newList)
                i+=1

        if user1 == user2:
            await addDeath(ctx, user1)
            embed=discord.Embed(color=0xfd5d5d)
            embed.add_field(name="Elimination", value=f'{user1.mention} {random.choice(funny)}', inline=False)
            embed.set_footer(text=f"{len(newList) - 1} Remaining")
            await ctx.send(embed=embed)
        else:
            await addKill(ctx, user1)
            await addDeath(ctx, user2)
            embed=discord.Embed(color=0xfd5d5d)
            embed.add_field(name="Elimination", value=f'{user1.mention} {random.choice(eliminations)} {user2.mention} with {random.choice(weapons)}', inline=False)
            embed.set_footer(text=f"{len(newList) - 1} Remaining")
            await ctx.send(embed=embed)
        
        # Updates the list by removing the user that got eliminated
        newList.remove(user2)

    await asyncio.sleep(3)

    await addWin(ctx, newList[0])

    embed=discord.Embed(title="Plunge", color=0xfd5d5d)
    embed.set_thumbnail(url=logourl)
    # TODO: Display the amount of kills
    embed.add_field(name="Battle Royale Victory", value=f'The winner of {ctx.guild.name}\'s Battle Royale is {newList[0].mention}\n\n{newList[0].mention} had {await getGameKills(ctx, newList[0])} kills', inline=False)
    embed.set_footer(text=f"{totalPlayers} players participated")
    await ctx.send(embed=embed)

    for player in PlayersForXp:
        await updateStats(ctx, player)

# Method that creates a new user object for json if they are not in the list
# TODO: Don't Pass the entire context... just pass the ctx.guild.id
# TODO: Check if the user is already in the list for faster response time
async def newUser(ctx, user):
    with open('userStats.json', 'r') as f:
        data = json.load(f)
    
    # if user is not in the list add a brand new user
    if str(user.id) not in list(data.keys()):

        serverId = {}
    
        serverId[ctx.guild.id] = {
            'wins': 0,
            'kills': 0,
            'deaths': 0,
            'currentGameKills': 0,
            'totalExp': 0,
            'color': 2433568
        }

        data[str(user.id)] = serverId

        with open('userStats.json', 'w') as f:
            json.dump(data, f, indent=4)

    # If user is in the list, check if the guild id is in the users guilds list
    else:
        # If the guild is in the users guilds list do nothing
        if str(ctx.guild.id) in list(data[str(user.id)].keys()):
            print(f'User already added for this server')
        
        # If the guild is not in the users guilds list, add new server stats
        else:
            serverId = {
                'wins': 0,
                'kills': 0,
                'deaths': 0,
                'currentGameKills': 0,
                'totalExp': 0,
                'color': 2433568
            }

            data[str(user.id)][str(ctx.guild.id)] = serverId

            with open('userStats.json', 'w') as f:
                json.dump(data, f, indent=4)

# Method that gets the current Game Kills
# TODO: Don't pass the ctx just pass ctx.guild.id
async def getGameKills(ctx, user):
    with open('userStats.json', 'r') as f:
        data = json.load(f)

    return data[str(user.id)][str(ctx.guild.id)]['currentGameKills']

# Method that updates your stats at the end of the game
# TODO: Don't pass the ctx just pass ctx.guild.id and Grab the user.id
async def updateStats(ctx, user):
    with open('userStats.json', 'r') as f:
        data = json.load(f)

    data[str(user.id)][str(ctx.guild.id)]['currentGameKills'] = 0

    wins = data[str(ctx.author.id)][str(ctx.guild.id)]['wins']
    kills = data[str(ctx.author.id)][str(ctx.guild.id)]['kills']
    deaths = data[str(ctx.author.id)][str(ctx.guild.id)]['deaths']
    gamesPlayed = deaths + wins

    totalExp = gamesPlayed * 10 + wins * 100 + kills * 25

    data[str(ctx.author.id)][str(ctx.guild.id)]['totalExp'] = totalExp

    with open('userStats.json', 'w') as f:
        json.dump(data, f, indent=4)

# Method that updates the users kills
# TODO: Don't pass the ctx just pass ctx.guild.id
async def addKill(ctx, user):
    with open('userStats.json', 'r') as f:
        data = json.load(f)

    data[str(user.id)][str(ctx.guild.id)]['kills'] += 1
    data[str(user.id)][str(ctx.guild.id)]['currentGameKills'] += 1

    with open('userStats.json', 'w') as f:
        json.dump(data, f, indent=4)

# Method that updates the users wins
# TODO: Don't pass the ctx just pass ctx.guild.id
async def addWin(ctx, user):
    with open('userStats.json', 'r') as f:
        data = json.load(f)

    data[str(user.id)][str(ctx.guild.id)]['wins'] += 1

    with open('userStats.json', 'w') as f:
        json.dump(data, f, indent=4)

# Method that updates the users deaths
# TODO: Don't pass the ctx just pass ctx.guild.id
async def addDeath(ctx, user):
    with open('userStats.json', 'r') as f:
        data = json.load(f)

    data[str(user.id)][str(ctx.guild.id)]['deaths'] += 1

    with open('userStats.json', 'w') as f:
        json.dump(data, f, indent=4)

# TODO: Method that calculates the users remaining experience to level and possibly display it??

# Command that fetches your stats for the server you are in
@client.command()
async def stats(ctx, param1 = None, param2 = None):
    await newUser(ctx, ctx.author)

    # If no parameters are passed in, 
    if param1 == None and param2 == None:

        # Creates User if it doesn't exist
        await newUser(ctx, ctx.author)

        # Display the users stats for this server
        await displayServerStats(ctx, ctx.author.id)

    elif param1.lower() == 'all' and param2 == None:

        # Creates User if it doesn't exist
        await newUser(ctx, ctx.author)

        # Display all the users stats
        await displayAllStats(ctx, ctx.author.id)

    elif param1 is not None and param2 == None:
        # Formats the Mention as a user ID
        param1 = param1.translate(dict.fromkeys(map(ord, '!@<>')))
        # Get the user object
        user = client.get_user(int(param1))

        if user is not None:
            # Creates stats for the user in this current server if it does not exist
            await newUser(ctx, user)

            # Display
            await displayServerStats(ctx, user.id)
        else:
            print('User not found')

    elif param1.lower() == 'all' and param2 is not None:
        # Formats the Mention as a user ID
        param2 = param2.translate(dict.fromkeys(map(ord, '!@<>')))
        # Get the user object
        user = client.get_user(int(param2))

        if user is not None:
            # Creates stats for the user in this current server if it does not exist
            await newUser(ctx, user)

            # Display
            await displayAllStats(ctx, user.id)
        else:
            print('User not found')
    


async def displayServerStats(ctx, authorId):
    with open('userStats.json', 'r') as f:
        data = json.load(f)

    wins = data[str(authorId)][str(ctx.guild.id)]['wins']
    kills = data[str(authorId)][str(ctx.guild.id)]['kills']
    deaths = data[str(authorId)][str(ctx.guild.id)]['deaths']
    totalExp = data[str(authorId)][str(ctx.guild.id)]['totalExp']

    # Gets the user
    user = client.get_user(authorId)

    # Gets the users avatar image
    avatarUrl = user.avatar_url

    if kills > 0 and deaths > 0:
        kd = kills / deaths
    elif deaths == 0:
        kd = kills
    else:
        kd = 0

    gamesPlayed = deaths + wins

    level = totalExp/100

    if wins > 0 and gamesPlayed > 0:
        winperc = wins / gamesPlayed * 100
    elif gamesPlayed == 0:
        winperc = 0
    else:
        winperc = 0

    color = data[str(user.id)][str(ctx.guild.id)]['color']

    embed=discord.Embed(title="Plunge Battle Royale Stats", color=color)
    embed.set_thumbnail(url=avatarUrl)
    embed.add_field(name=f"Level: {math.floor(level)}", value=f"{user.mention}\n\nWins: {wins}\nKills: {kills}\nDeaths: {deaths}\nK/D Ratio: {round(kd, 2)}\nGames Played: {gamesPlayed}\nWin Percentage: {round(winperc)}%", inline=False)
    embed.set_footer(text=f"Stats for: {ctx.guild.name}")
    await ctx.send(embed=embed)

async def displayAllStats(ctx, authorId):

    with open('userStats.json', 'r') as f:
        data = json.load(f)

    wins = 0
    kills = 0
    deaths = 0
    totalExp = 0

    authorId = str(authorId)

    for server in list(data[authorId]):
        serverId = str(server)
        wins += data[authorId][serverId]['wins']
        kills += data[authorId][serverId]['kills']
        deaths += data[authorId][serverId]['deaths']
        totalExp += data[authorId][serverId]['totalExp']

    # Gets the user
    user = client.get_user(int(authorId))

    # Gets the users avatar image
    avatarUrl = user.avatar_url

    if kills > 0 and deaths > 0:
        kd = kills / deaths
    elif deaths == 0:
        kd = kills
    else:
        kd = 0

    gamesPlayed = deaths + wins

    level = totalExp/100

    if wins > 0 and gamesPlayed > 0:
        winperc = wins / gamesPlayed * 100
    elif gamesPlayed == 0:
        winperc = 0
    else:
        winperc = 0

    color = data[str(user.id)][str(ctx.guild.id)]['color']

    embed=discord.Embed(title="Plunge Battle Royale Stats", color=color)
    embed.set_thumbnail(url=avatarUrl)
    embed.add_field(name=f"Level: {math.floor(level)}", value=f"{user.mention}\n\nWins: {wins}\nKills: {kills}\nDeaths: {deaths}\nK/D Ratio: {round(kd, 2)}\nGames Played: {gamesPlayed}\nWin Percentage: {round(winperc)}%", inline=False)
    embed.set_footer(text=f"All Stats")
    await ctx.send(embed=embed)

# Runs the bot
client.run(data['token'])