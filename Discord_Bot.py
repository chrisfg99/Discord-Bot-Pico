#Christopher Greer 
#03/01/2023
#Discord Bot

import random
import discord
from discord.ext import commands
import json

#try reading settings from json file
try:
    with open("config.json", 'r') as f:
        data = json.load(f)
except:
    print("No file found, make sure it is in the same folder")

# Server token here
TOKEN = data["TOKEN"]
# channel for welcome messages
WELCOME_CHANNEL = data["WELCOME_CHANNEL"]
#rules channel
RULES_CHANNEL = data["RULES_CHANNEL"]
# list of names for the random_name command
NAMES = data["NAMES"]
# list of join messaages for the join command
JOINS = data["JOINS"]
#permission to ban members
ban_members = data["ban_members"]
#permission to kick users
kick_members = data["kick_members"]
#permission to manage nicknames
manage_nicknames= data["manage_nicknames"]
#command prefix
intents = discord.Intents.all() 
bot = commands.Bot(command_prefix=data["prefix"],intents=intents)


#Startup Notification
@bot.event
async def on_ready():
    print("bot has started")

#Make random and show rules channel
#Member Join Notification
@bot.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.channels,
                                        name=WELCOME_CHANNEL)
    # feel free to change this message!
    await welcome_channel.send(
        f"welcome {member.mention}, please read our rules and have a great time!")

#Ban User command
@commands.has_permissions(ban_members=ban_members)
@bot.command()
async def ban(ctx, user: discord.Member):
    """Ban the given user"""
    await ctx.guild.ban(user, delete_message_days=0)
    await ctx.send(f"banned {user}")

#Unban User command
@commands.has_permissions(ban_members=ban_members)
@bot.command()
async def unban(ctx, user: discord.User):
    "Unban the given user"
    await ctx.guild.unban(user)
    await ctx.send(f"unbanned {user}")

#Kick users
@commands.has_permissions(kick_members=kick_members)
@bot.command()
async def kick(ctx, user: discord.User):
    "Kick the given user"
    await ctx.guild.kick(user)
    await ctx.send(f"kicked {user}")

#command to randomise nicknames
@bot.command(aliases=["rnick"])
async def random_nick(ctx):
    """Set your nickname to a random one"""
    new_nick = random.choice(NAMES)
    await ctx.author.edit(nick=new_nick)
    await ctx.send(f"Your new nickname is {new_nick}")

#Command to change someonelses nickname
@commands.has_permissions(manage_nicknames=manage_nicknames)
@bot.command(aliases=["change_name"])
async def change_nick(ctx, user: discord.Member, *, new_nick):
    """Change somebody elses nickname."""
    await user.edit(nick=new_nick)
    await ctx.send(f"Changed the nick of {user.mention} to `{new_nick}`")

#Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
