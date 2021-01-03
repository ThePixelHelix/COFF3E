import discord
from colorama import Fore, init
import os
import asyncio
from discord.ext import commands


class Suggest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

  
    @commands.command()
    @commands.guild_only()
    async def suggest(self, ctx,*,suggestion):
      
      SuggestE = discord.Embed(
        colour=0xff63b7,
        title=f"💭 New suggestion!",
        description=f"{suggestion}"
      )
      SuggestE.set_footer(text=f"Made by llama • Suggested by {ctx.author.name}", icon_url=str(ctx.author.avatar_url_as(static_format='png', size=2048)))
      SuggestE.set_thumbnail(url=self.bot.thumbnail)
      
      channel = discord.utils.get(ctx.guild.channels, id=748091309193166858)
      await ctx.channel.purge(limit=1)
      message = await channel.send(embed=SuggestE)
      thumbsup = '<:check:748051080151171164>'
      thumbsdown = '<:cross:748051156890026015>'
      await message.add_reaction(thumbsup)
      await message.add_reaction(thumbsdown)



def setup(bot):
    try:
      bot.add_cog(Suggest(bot))
      print(f'{Fore.GREEN}Loaded suggest command!')
    except Exception as e:
      print(f'{Fore.RED}Error while adding command suggest', e)