import discord
from discord.ext import commands
from colorama import Fore, Style
from webserver import keep_alive
import os
import traceback
import random
import asyncio
import sqlite3

def coffee_prefix(bot, message):
  return commands.when_mentioned_or('c/','C/')(bot, message)

extensions = [
  "commands.help",
  "commands.hex",
  "commands.info",
  "commands.ping",
  "commands.steal",
  "commands.music",
  "commands.suggest",
  "events.convo_sano",
  "events.convo_why",
  "events.message_delete",
  "events.message_edit",
  "levelsys.ranking"
]
TOKEN = os.environ.get("DISCORD_BOT_SECRET")

bot = commands.Bot(
    command_prefix=coffee_prefix,
    status=discord.Status.do_not_disturb,
    activity=discord.Streaming(name=f"hot coffee", url="https://twitch.tv/llamaWol"),
    case_insensitive=True,
    owner_id=625276939845763082,
    max_messages=2500,
    fetch_offline_members=False,
    dev=False,
    allowed_mentions=discord.AllowedMentions(
        everyone=False, users=False, roles=False)
)

@bot.event
async def on_ready():
  db = sqlite3.connect("resources/main.db")
  cursor = db.cursor()
  cursor.execute(
    """CREATE TABLE IF NOT EXISTS "glevel" (
    "enabled" TEXT,
    "guild_id" TEXT,
    "user_id" TEXT,
    "exp" TEXT,
    "level" TEXT
    );"""
    )
  cursor.execute(
    """CREATE TABLE IF NOT EXISTS "tlevel" (
    "guild_id" TEXT,
    "user_id" TEXT,
    "xp_time" TEXT
    );"""
    )
  cursor.execute(
    """CREATE TABLE IF NOT EXISTS "vlevel" (
    "channel_id" TEXT,
    "guild_id" TEXT,
    "user_id" TEXT,
    "start_time" TEXT,
    "join_time" TEXT
    );"""
    )
  cursor.execute(
    """CREATE TABLE IF NOT EXISTS "ranks" (
    "guild_id" TEXT,
    "role_id" TEXT,
    "level" TEXT
    );"""
    )

  for cog in extensions:
    try:
      print(f'\n{Style.BRIGHT}{Fore.LIGHTYELLOW_EX}Loading cog {cog}...{Style.RESET_ALL}\n')
      bot.load_extension(cog)
    except Exception as e:
      print(f"{Fore.RED}Error while loading {cog}", e)
    
  print(f"\n{Style.BRIGHT}{Fore.CYAN}==============================")
  print(f"\nBot: {Fore.LIGHTYELLOW_EX}{bot.user}")
  print(f"{Fore.CYAN}ID: {Fore.LIGHTYELLOW_EX}{bot.user.id}")
  print(f"{Fore.CYAN}Guilds: {Fore.LIGHTYELLOW_EX}{len(bot.guilds)}")
  print(f"{Fore.CYAN}Users: {Fore.LIGHTYELLOW_EX}{len(bot.users)}")
  print(f"\n{Fore.CYAN}=============================={Style.RESET_ALL}")


bot.thumbnail = random.choice(["https://cdn.discordapp.com/attachments/747410626816507998/747513863796293852/IMG_4816.PNG","https://cdn.discordapp.com/attachments/747410626816507998/747513863662075904/IMG_4828.PNG","https://cdn.discordapp.com/attachments/747410626816507998/747513863615807979/IMG_4815.PNG","https://cdn.discordapp.com/attachments/747410626816507998/747513863561281686/IMG_4817.PNG","https://cdn.discordapp.com/attachments/747410626816507998/747513863620132874/IMG_4812.PNG","https://cdn.discordapp.com/attachments/747410626816507998/747513863548698748/IMG_4814.PNG","https://cdn.discordapp.com/attachments/747410626816507998/747513863741767732/IMG_4823.PNG","https://cdn.discordapp.com/attachments/747410626816507998/747513863695761890/IMG_4819.PNG","https://cdn.discordapp.com/attachments/747410626816507998/747513864169717860/IMG_4813.PNG","https://cdn.discordapp.com/attachments/747410626816507998/747513863980711976/IMG_4821.PNG","https://cdn.discordapp.com/attachments/747410626816507998/747529227846287480/IMG_4840.PNG","https://cdn.discordapp.com/attachments/747410626816507998/747529227989155950/IMG_4841.PNG","https://cdn.discordapp.com/attachments/747410626816507998/747712665715212308/IMG_4841.PNG","https://cdn.discordapp.com/attachments/747410626816507998/747712665899630592/IMG_4854.PNG","https://cdn.discordapp.com/attachments/747410626816507998/747712666763788358/IMG_4856.PNG","https://cdn.discordapp.com/attachments/747410626816507998/747712666734166056/IMG_4858.PNG","https://cdn.discordapp.com/attachments/747410626816507998/747712666780303471/IMG_4857.PNG","https://cdn.discordapp.com/attachments/747410626816507998/747715319644028978/IMG_4860.PNG"])


@bot.event
async def on_member_join(member):
  if member.bot:
    return False
  member_count = len(member.guild.members)
  WelcomeE = discord.Embed(
    colour=0xff63b7,
    title=f"**<:Sano:747894539452284968> Welcome to {member.guild}!**",
    description=f"Welcome {member.name}!\n\nPlease make sure to read <#747843073182269510> and pick your roles in <#747890092848185487>"
  )
  WelcomeE.set_thumbnail(url=bot.thumbnail)
  WelcomeE.set_footer(text=f"Made by llama", icon_url=str(member.avatar_url_as(static_format='png', size=2048)))
  channel = bot.get_channel(id=747808128363659276)
  await(await channel.send(embed = WelcomeE)).delete(delay=120)
  mcount = discord.utils.get(member.guild.channels, id=748227781636129145)
  await mcount.edit(name=f'Refugees | {member_count}')


@bot.event
async def on_member_remove(member):
  if member.bot:
    return False
  member_count = len(member.guild.members)
  LeaveE = discord.Embed(
    colour=0xff63b7,
    title=f"**🚪 Someone left us!**",
    description=f"{member.name} left the server\n\nWe now have {membercount} members left"
  )
  LeaveE.set_thumbnail(url=bot.thumbnail)
  LeaveE.set_footer(text=f"Made by llama", icon_url=str(member.avatar_url_as(static_format='png', size=2048)))
  channel = bot.get_channel(id=747808128363659276)
  await(await channel.send(embed = LeaveE)).delete(delay=120)
  mcount = discord.utils.get(member.guild.channels, id=748227781636129145)
  await mcount.edit(name=f'Refugees | {member_count}')

bot.run(TOKEN)
keep_alive()
bot.loop.create_task(change_status())
