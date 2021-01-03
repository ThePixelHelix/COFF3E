from discord.ext import commands
from colorama import Fore, init
import discord
import random


class Convo_sano(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
      if message.author.bot: 
        return False
      if message.content == "<:Sano:747894539452284968>":
        if random.random() < 0.8:
          await message.channel.send("<:Sano:747894539452284968>")


def setup(bot):
    try:
        bot.add_cog(Convo_sano(bot))
        print(f'{Fore.GREEN}Loaded convo_sano event!')
    except Exception as e:
        print(f'{Fore.RED}Error while adding event convo_sano', e)