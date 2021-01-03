import discord
from discord.ext import commands
from collections import OrderedDict, deque, Counter
from colorama import Fore, init
import os
import math
import random


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["ui"])
    @commands.guild_only()
    async def userinfo(self, ctx,member:discord.Member=None):
      if member == None:
        member=ctx.author
      if member.bot==True:
        bot="true"
      else:
        bot="false"
      
      UserinfoE = discord.Embed(
        colour=0xff63b7,
        title=f"Userinfo **»** {member.name}",
        description=f"- ID **{member.id}**\n- Nickname **{member.display_name}**\n- Name color **{member.color}**\n- Bot **{bot}**\n\n- Created At **{member.created_at.strftime('%d/%m/%Y, %I:%m %p')}**\n- Join Date **{member.joined_at.strftime('%d/%m/%Y, %I:%m %p')}**"
      )
      UserinfoE.set_thumbnail(url=str(member.avatar_url_as(static_format='png', size=2048)))
      UserinfoE.set_footer(text=f"Made by llama • Requested by {ctx.author.name}", icon_url=str(ctx.author.avatar_url_as(static_format='png', size=2048)))
      await ctx.send(embed=UserinfoE)
      
      
    @commands.command(aliases=["si"])
    @commands.guild_only()
    async def serverinfo(self, ctx):
        total_member_count = len(ctx.guild.members)
        human_count = len([m for m in ctx.guild.members if not m.bot])
        bot_count = math.floor(total_member_count-human_count)
  
        ServerinfoE = discord.Embed(
          colour=0xff63b7,
          title=f"Serverinfo **»** {ctx.guild.name}",
          description=f"- Owner **{ctx.guild.owner}**\n\n- Name **{ctx.guild.name}**\n- ID **{ctx.guild.id}**\n\n- Created At **{ctx.guild.created_at.strftime('%d/%m/%Y, %I:%m %p')}**\n- Region **{ctx.guild.region}**\n\n- All Members **{total_member_count}**\n- Humans **{human_count}**\n- Bots **{bot_count}**\n\n- Categories **{len(ctx.guild.categories)}**\n- Text Channels **{len(ctx.guild.text_channels)}**\n- Voice Channels **{len(ctx.guild.voice_channels)}**\n\n- Roles **{len(ctx.guild.roles)}**\n- Emojis **{len(ctx.guild.emojis)}**\n\n- Boosts **{ctx.guild.premium_subscription_count}**\n- Level **{ctx.guild.premium_tier}**"
        )
        ServerinfoE.set_thumbnail(url=str(ctx.guild.icon_url_as(static_format='png', size=2048)))
        ServerinfoE.set_footer(text=f"Made by llama • Requested by {ctx.author.name}", icon_url=str(ctx.author.avatar_url_as(static_format='png', size=2048)))
        await ctx.send(embed=ServerinfoE)
        
        
    @commands.command(aliases=["ri"])
    @commands.guild_only()
    async def roleinfo(self, ctx,role:discord.Role=None):
      RoleinfoE = discord.Embed(
        colour=0xff63b7,
        title=f"Roleinfo **»** {role.name}",
        description=f"- ID **{role.id}**\n- Color **{role.color}**\n- Position **#{role.position}**\n- Users **{len(role.members)}**\n\n- Created At **{role.created_at.strftime('%d/%m/%Y, %I:%m %p')}**"
      )
      RoleinfoE.set_thumbnail(url=str(ctx.guild.icon_url_as(static_format='png', size=2048)))
      RoleinfoE.set_footer(text=f"Made by llama • Requested by {ctx.author.name}", icon_url=str(ctx.author.avatar_url_as(static_format='png', size=2048)))
      await ctx.send(embed=RoleinfoE)


    @commands.command(aliases=["bi"])
    @commands.guild_only()
    async def botinfo(self, ctx):
      coffee = discord.Embed(
        colour=0xff63b7,
        title=f"Botinfo **»** COFF3E",
        description=f"- Total Servers **{len(list(self.bot.guilds))}**\n- Total Users **{len(list(self.bot.users))}**\n- Ping **{round(self.bot.latency*1000)}ms**\n\n- Python Version **3.8.2**\n- Discord.py Version **{discord.__version__}**")
      coffee.set_footer(text=f"Made by llama • Requested by {ctx.author.name}", icon_url=str(ctx.author.avatar_url_as(static_format='png', size=2048)))
      coffee.set_thumbnail(url=self.bot.thumbnail)
      await ctx.send(embed=coffee)
    

def setup(bot):
    try:
        bot.add_cog(Info(bot))
        print(f'{Fore.GREEN}Loaded info commands!')
    except Exception as e:
        print(f'{Fore.RED}Error while adding commands info', e)