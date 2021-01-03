from discord.ext import commands
from colorama import Fore, init
import discord
import random


class Message_edit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
      if message_after.author.bot: 
        return False
      EditedmsgE=discord.Embed(
        colour=0xff63b7,
        title="A message was edited!",
        description=f"**Author** » {message_after.author}\n**Channel** » <#{message_after.channel.id}>\n**Content before** » {message_before.content}\n**Content after** » {message_after.content}"
      )
      EditedmsgE.set_thumbnail(url=self.bot.thumbnail)
      EditedmsgE.set_footer(text=f"Made by llama", icon_url=str(message_after.author.avatar_url_as(static_format='png', size=2048)))
      
      channel = discord.utils.get(message_after.guild.channels, id =747885481546481665)
      await channel.send(embed = EditedmsgE)


def setup(bot):
    try:
        bot.add_cog(Message_edit(bot))
        print(f'{Fore.GREEN}Loaded message_edit event!')
    except Exception as e:
        print(f'{Fore.RED}Error while adding event message_edit', e)