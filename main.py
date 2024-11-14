from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from termcolor import colored

load_dotenv()

owner_id = int(os.getenv("OWNER_ID"))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    commands_list = [command.name for command in bot.commands]
    print("Available Commands:")
    for command in commands_list:
        print(f' - {command}')

    print("Servers:")
    for guild in bot.guilds:
        print(f' - {guild.name} (ID: {guild.id})')

    # Afficher un message stylisé
    bot_name = bot.user.name
    print(colored(f'Bot {bot_name} prêt à l\'utilisation !', 'green', attrs=['bold']))

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Cleared {amount} messages', delete_after=5)

@bot.command()
async def restart(ctx):
    if ctx.author.id == owner_id:
        await ctx.send('Restarting...')
        await bot.close()
        os.system(f"python {__file__}")
    else:
        await ctx.send(f'You do not have permission to restart the bot.')

@bot.command()
async def get_id(ctx):
    await ctx.send(f'Your ID: {ctx.author.id}')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

bot.run(os.getenv("BOT_TOKEN"))