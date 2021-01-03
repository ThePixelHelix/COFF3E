import discord
from discord.ext import commands
from colorama import Fore, init
import os
import math
import random


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):
      PingE = discord.Embed(
        colour=0xff63b7,
        title="🏓 Pong!",
        description=f"My ping is {round(self.bot.latency*1000)}ms"
      )
      PingE.set_footer(text=f"Made by llama • Requested by {ctx.author.name}", icon_url=str(ctx.author.avatar_url_as(static_format='png', size=2048)))
      PingE.set_thumbnail(url=self.bot.thumbnail)
      await ctx.send(embed=PingE)


def setup(bot):
    try:
        bot.add_cog(Ping(bot))
        print(f'{Fore.GREEN}Loaded ping command!')
    except Exception as e:
        print(f'{Fore.RED}Error while adding command ping', e)