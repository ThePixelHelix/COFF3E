from discord.ext import commands
from colorama import Fore, init
import discord
import random


class Convo_why(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
      if message.author.bot: 
        return False
      if message.content.split()[0].lower() == "why":
        if random.random() < 0.2:
          await message.channel.send(random.choice(["Because coffee in a cup","Because why not?","Because I said so","Because thats the way it is"]))


def setup(bot):
    try:
        bot.add_cog(Convo_why(bot))
        print(f'{Fore.GREEN}Loaded convo_why event!')
    except Exception as e:
        print(f'{Fore.RED}Error while adding event convo_why', e)