from colorama import Fore, init
from discord.ext import commands
import discord
import typing
import random


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")


    @commands.command()
    @commands.guild_only()
    async def help(self, ctx):
      HelpE = discord.Embed(
        colour=0xff63b7,
        title="**<:question:748051203170107472> Help has arrived!**",
        description="Misc\n- **Help »** Sends you this message\n- **Ping »** Check how much ping I have\n- **Color »** Get a preview of a hex code\n\nInfo\n- **Userinfo »** Shows info about mentioned user\n- **Serverinfo »** Shows serverinfo\n- **Roleinfo »** Shows info about mentioned role\n- **Botinfo »** Shows info about me"
      )
      HelpE.set_footer(text=f"Made by llama • Requested by {ctx.author.name}", icon_url=str(ctx.author.avatar_url_as(static_format='png', size=2048)))
      HelpE.set_thumbnail(url=self.bot.thumbnail)
      await ctx.send(embed=HelpE)


def setup(bot):
    try:
        bot.add_cog(Help(bot))
        print(f'{Fore.GREEN}Loaded help command!')
    except Exception as e:
        print(f'{Fore.RED}Error while adding command help', e)