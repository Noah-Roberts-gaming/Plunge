import discord
from discord.ext import commands, tasks
import random
import json
import asyncio

# The prefix for all the commands
prefix = "p."
activeBattles = []
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
    elif isinstance(error, commands.MissingPermissions):
        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Missing Permissions", value="To verify for the User role in the Plunge Development server, you need to be an administrator or have permissions to manage the server you are currently in.", inline=False)
        embed.add_field(name="To Verify", value="[Invite the bot](https://discord.com/api/oauth2/authorize?client_id=732864657932681278&permissions=313408&scope=bot) to a server you own or are administrator of and use `p.verify` there.", inline=False)
        await ctx.send(embed=embed)
    else:
        raise error


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
        embed.add_field(name="General", value=f"`{prefix}drop` `{prefix}help` `{prefix}feedback` `{prefix}invite` `{prefix}discord` `{prefix}verify` `{prefix}giveaway`", inline=False)
        embed.add_field(name="Info", value=f"To get more help on a command or see the command's function, try: `p.help (command)`", inline=False)
        await ctx.send(embed=embed)
    elif setting.lower() == "drop":
        embed=discord.Embed(title="Plunge", description="Drop Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Gives you a random location to drop in Fortnite!", inline=False)
        embed.add_field(name="Usage:", value="`p.drop`", inline=False)
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
    elif setting.lower() == "discord" or setting.lower() == "server" or setting.lower() == "join" or setting.lower() == "support":
        embed=discord.Embed(title="Plunge", description="Discord Command", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Description:", value=f"Invites you to the bot's development server!", inline=False)
        embed.add_field(name="Usage:", value=f"`p.{setting}`", inline=False)
        embed.add_field(name="Aliases:", value="`p.discord`, `p.server`, `p.join`, `p.support`", inline=False)
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
        reply.add_field(name="Suggestion Sent", value="Thanks for submitting your suggestion!", inline=False)
        reply.set_footer(text="p.invite • Invites this bot to your server")
        await ctx.send(embed=reply)
        
        # Suggestion added to suggestions channel
        suggested=discord.Embed(title="Plunge", description=f"Submitted by {ctx.author.name}#{ctx.author.discriminator}", color=0xfd5d5d)
        suggested.set_thumbnail(url=ctx.author.avatar_url)
        suggested.add_field(name="Suggestion", value=suggestion, inline=False)
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

# Command that simulates a battle royale
# p.battle
@client.command()
async def battle(ctx, param = None):
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
        embed.add_field(name="Battle Starting", value="React to the message below to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 30 seconds!", inline=False)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('<:plunge:734656507194507275>')

        await asyncio.sleep(10)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value="React to the message below to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 20 seconds!", inline=False)
        await msg.edit(embed=embed)

        await asyncio.sleep(10)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value="React to the message below to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 10 seconds!", inline=False)
        await msg.edit(embed=embed)

        await asyncio.sleep(5)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value="React to the message below to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 5 seconds!", inline=False)
        await msg.edit(embed=embed)

        await asyncio.sleep(1)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value="React to the message below to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 4 seconds!", inline=False)
        await msg.edit(embed=embed)

        await asyncio.sleep(1)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value="React to the message below to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 3 seconds!", inline=False)
        await msg.edit(embed=embed)

        await asyncio.sleep(1)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value="React to the message below to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 2 seconds!", inline=False)
        await msg.edit(embed=embed)

        await asyncio.sleep(1)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle Starting", value="React to the message below to be entered in this battle royale.", inline=False)
        embed.add_field(name="Ready Up!", value="We are starting in 1 seconds!", inline=False)
        await msg.edit(embed=embed)

        await asyncio.sleep(1)

        embed=discord.Embed(title="Plunge", color=0xfd5d5d)
        embed.set_thumbnail(url=logourl)
        embed.add_field(name="Battle In Progress...", value="Good Luck Everyone!", inline=False)
        await msg.edit(embed=embed)

        # Caches your message so you can get the reactions
        cache_msg = discord.utils.get(client.cached_messages, id = msg.id)
        
        # loops through the reactions
        for reaction in cache_msg.reactions:
            # if reaction is the plunge emoji...
            if str(reaction.emoji) == '<:plunge:734656507194507275>':
                # Grabs the users that used that reaction
                users = await reaction.users().flatten()
                # loops through each user
                for user in users:
                    print(user.name)
                    await ctx.send(user.name)


        # removes the guild from the active battles check (this comes last)
        activeBattles.remove(ctx.guild.id)


# Runs the bot
client.run(data['token'])