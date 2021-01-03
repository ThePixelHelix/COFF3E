from discord.ext import commands
from colorama import Fore, init
import discord
import random


class Message_delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message_delete(self, message):
      if message.author.bot: 
        return False
      DelmsgE= discord.Embed(
        colour=0xff63b7,
        title="A message was deleted!",
        description=f"**Author** » {message.author}\n**Channel** » <#{message.channel.id}>\n**Content** » {message.content}"
      )
      DelmsgE.set_thumbnail(url=self.bot.thumbnail)
      DelmsgE.set_footer(text=f"Made by llama", icon_url=str(message.author.avatar_url_as(static_format='png', size=2048)))
      channel = discord.utils.get(message.guild.channels, id=747885481546481665)
      await channel.send(embed = DelmsgE)


def setup(bot):
    try:
        bot.add_cog(Message_delete(bot))
        print(f'{Fore.GREEN}Loaded message_delete event!')
    except Exception as e:
        print(f'{Fore.RED}Error while adding event message_delete', e)