import discord
from colorama import Fore, init
import os
import random
import asyncio
from discord.ext import commands


class Hex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

  
    @commands.command(aliases=["colour","hex"])
    @commands.guild_only()
    async def color(self, ctx,*,color:str):

      HexE = discord.Embed(
        colour=0xff63b7,
        title=f"Hex color **»** #{color}"
      )
      HexE.set_footer(text=f"Made by llama • Requested by {ctx.author.name}", icon_url=str(ctx.author.avatar_url_as(static_format='png', size=2048)))
      HexE.set_image(url=f"https://dummyimage.com/1920x1080/{color}/{color}.png")
      HexE.set_thumbnail(url=self.bot.thumbnail)
      await ctx.send(embed=HexE)


def setup(bot):
    try:
        bot.add_cog(Hex(bot))
        print(f'{Fore.GREEN}Loaded hex command!')
    except Exception as e:
        print(f'{Fore.RED}Error while adding command hex', e)