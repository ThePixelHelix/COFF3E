import discord
from discord import File
from discord.ext import commands
from colorama import Fore, init
import asyncio
import datetime
import sqlite3
import os
import time
from collections import OrderedDict, deque, Counter
import math
import random
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import io
from io import BytesIO
import requests
import aiohttp
from .utils import checks


class Ranks(commands.Cog, name='Ranks'):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @checks.is_admin()
    async def levelrole(self, ctx):
        await ctx.send('**Levelrole Commands**\n\nlevelrole add\nlevelrole remove\nlevelrole list')
    
    @levelrole.command()
    @checks.is_admin()
    async def add(self, ctx):
        await ctx.send('**Please insert the role name.** *(Case Sensitive)*')
        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.message.channel
        rolename = await self.bot.wait_for('message', check=check)
        await ctx.send('**Please insert the level required to obtain this role.**')
        level = await self.bot.wait_for('message', check=check)
        role = discord.utils.get(ctx.guild.roles, name=rolename.content)
        main = sqlite3.connect('resources/main.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT role_id, level FROM ranks WHERE guild_id = '{ctx.guild.id}' and role_id = '{role.id}'")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO ranks(guild_id, role_id, level) VALUES(?,?,?)")
            val = (str(ctx.guild.id), str(role.id), level.content)
            cursor.execute(sql, val)
            main.commit()
            await ctx.send('Role added.')
        else:
            await ctx.error('That role is already assigned to a level.')
        cursor.close()
        main.close()
    
    @levelrole.command()
    @checks.is_admin()
    async def remove(self, ctx):
        await ctx.send('**Please insert the role name.** *(Case Sensitive)*')
        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.message.channel
        rolename = await self.bot.wait_for('message', check=check)
        role = discord.utils.get(ctx.guild.roles, name=rolename.content)
        main = sqlite3.connect('resources/main.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT role_id, level FROM ranks WHERE guild_id = '{ctx.guild.id}' and role_id = '{role.id}'")
        result = cursor.fetchone()
        if result is not None:
            cursor.execute("DELETE FROM ranks WHERE guild_id = '{}' and role_id = '{}'".format(ctx.guild.id, role.id))
            main.commit()
            await ctx.send('Role removed.')
        else:
            await ctx.send('That role is not assigned to a level.')
        cursor.close()
        main.close()
    
    @levelrole.command(name='list')
    @checks.is_admin()
    async def _list(self, ctx):
        main = sqlite3.connect('resources/main.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT role_id, level FROM ranks WHERE guild_id = '{ctx.guild.id}'")
        result = cursor.fetchall()
        ranks = ''
        for result in result:
            role = ctx.guild.get_role(int(result[0]))
            ranks += f'{role.name} - {str(result[1])}\n'
        await ctx.send(ranks)


class TextLeveling(commands.Cog, name='Leveling'):

    def __init__(self, bot):
        self.bot = bot

    async def ranking(self, message):
        main = sqlite3.connect('resources/main.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT role_id, level FROM ranks WHERE guild_id = '{message.guild.id}'")
        result = cursor.fetchall()
        cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
        result1 = cursor.fetchone()
        lvl = int(result1[2])
        for result in result:
            role = message.guild.get_role(int(result[0]))
            try:
                if lvl >= int(result[1]):
                    await message.author.add_roles(role)
            except:
                return


    @commands.Cog.listener()
    async def on_member_join(self, member):
        main = sqlite3.connect('resources/main.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{member.guild.id}' and user_id = '{member.id}'")
        result1 = cursor.fetchone()
        if result1 is None:
          sql = ("INSERT INTO glevel(guild_id, user_id, exp, level) VALUES(?,?,?,?)")
          val = (str(member.guild.id), str(member.id), 0, 0)
          cursor.execute(sql, val)
          sql = ("INSERT INTO tlevel(guild_id, user_id, xp_time) VALUES(?,?,?)")
          val = (str(member.guild.id), str(member.id), datetime.datetime.utcnow())
          cursor.execute(sql, val)
          main.commit()
        if result1 is not None:
          return
        cursor.close()
        main.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            main = sqlite3.connect('resources/main.db')
            cursor = main.cursor()
            cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
            result1 = cursor.fetchone()
            if result1 is None:
              sql = ("INSERT INTO glevel(guild_id, user_id, exp, level) VALUES(?,?,?,?)")
              val = (str(message.guild.id), str(message.author.id), 0, 0)
              cursor.execute(sql, val)
              sql = ("INSERT INTO tlevel(guild_id, user_id, xp_time) VALUES(?,?,?)")
              val = (str(message.guild.id), str(message.author.id), datetime.datetime.utcnow())
              cursor.execute(sql, val)
              main.commit()
              await TextLeveling(self).ranking(message) 
            else:
              cursor.execute(f"SELECT xp_time FROM tlevel WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
              result2 = cursor.fetchone()
              datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
              time_diff = datetime.datetime.strptime(str(datetime.datetime.utcnow()), datetimeFormat) - datetime.datetime.strptime(str(result2[0]), datetimeFormat)
              if time_diff.seconds >= 60:
                exp = int(result1[1])
                sql = ("UPDATE glevel SET exp = ? WHERE guild_id = ? and user_id = ?")
                val = (int(exp + random.randint(10,21)), str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                sql = ("UPDATE tlevel SET xp_time = ? WHERE guild_id = ? and user_id = ?")
                val = (datetime.datetime.utcnow(), str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                main.commit()
                cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
                result2 = cursor.fetchone()
                xp_start = int(result2[1])
                lvl_start = int(result1[2])
                        
                xp_end = math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)
                if xp_end < xp_start:               
                  await message.channel.send(f'Jeez! Stop drinking coffee {message.author.mention}, you\'re already at {lvl_start + 1} cup(s)')
                  sql = ("UPDATE glevel SET level = ? WHERE guild_id = ? and user_id = ?")
                  val = (int(lvl_start + 1), str(message.guild.id), str(message.author.id))
                  cursor.execute(sql, val)
                  main.commit()
                  sql1 = ("UPDATE glevel SET exp = ? WHERE guild_id = ? and user_id = ?")
                  val1 = (xp_start - xp_end, str(message.guild.id), str(message.author.id))  
                  cursor.execute(sql1, val1)
                  main.commit()
                  await TextLeveling(self).ranking(message)
                else:
                  await TextLeveling(self).ranking(message)


class VoiceLeveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def ranking(self, member, user):
        main = sqlite3.connect('resources/main.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT role_id, level FROM ranks WHERE guild_id = '{member.guild.id}'")
        result = cursor.fetchall()
        cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{member.guild.id}' and user_id = '{user.id}'")
        result1 = cursor.fetchone()
        lvl = int(result1[2])
        for result in result:
            role = member.guild.get_role(int(result[0]))
            try:
                if lvl >= int(result[1]):
                    await user.add_roles(role)
            except:
                return

    async def start_time(self, member, before, after):
        if sum(1 for m in after.channel.members if not m.bot) >= 2:
            main = sqlite3.connect('resources/main.db')
            cursor = main.cursor()
            cursor.execute(f"SELECT channel_id, user_id FROM vlevel WHERE guild_id = '{member.guild.id}' and channel_id = '{after.channel.id}'")
            result = cursor.fetchall()
            for result in result:
                user = member.guild.get_member(int(result[1]))
                cursor.execute(f"SELECT start_time FROM vlevel WHERE guild_id = '{member.guild.id}' and user_id = '{user.id}' and channel_id = '{after.channel.id}'")
                result = cursor.fetchone()
                if result[0] is None or str(result[0]) == 'none':
                    sql = ("UPDATE vlevel SET start_time = ? WHERE guild_id = ? and user_id = ?")
                    val = (datetime.datetime.utcnow(), str(member.guild.id), str(user.id))
                    cursor.execute(sql, val)
                    main.commit()
                else:
                    if user in after.channel.members:
                        cursor.close()
                        main.close()
                        await VoiceLeveling(self).stop_time(member,before, after)
                        main = sqlite3.connect('resources/main.db')
                        cursor = main.cursor()
                        sql = ("UPDATE vlevel SET start_time = ? WHERE guild_id = ? and user_id = ?")
                        val = (datetime.datetime.utcnow(), str(member.guild.id), str(user.id))
                        cursor.execute(sql, val)
                        main.commit()
                    else:
                        continue
            cursor.close()
            main.close()
        else:
            return

    async def stop_time(self, member, before, after):
        main = sqlite3.connect('resources/main.db')
        cursor = main.cursor()
        if before.channel is None:
            cursor.execute(f"SELECT channel_id, user_id FROM vlevel WHERE guild_id = '{member.guild.id}' and channel_id = '{after.channel.id}'")
            result = cursor.fetchall()
            members = after.channel.members
        else:
            cursor.execute(f"SELECT channel_id, user_id FROM vlevel WHERE guild_id = '{member.guild.id}' and channel_id = '{before.channel.id}'")
            result = cursor.fetchall()
            members = before.channel.members
        cursor.close()
        main.close()
        for result in result:
            main = sqlite3.connect('resources/main.db')
            cursor = main.cursor()
            user = member.guild.get_member(int(result[1]))
            if user not in members:
                cursor.execute(f"SELECT start_time FROM vlevel WHERE guild_id = '{member.guild.id}' and user_id = '{user.id}'")
                result2 = cursor.fetchone()
                datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
                time_diff = datetime.datetime.strptime(str(datetime.datetime.utcnow()), datetimeFormat) - datetime.datetime.strptime(str(result2[0]), datetimeFormat)
                xp = 0
                minutes = int(time_diff.seconds) / 60
                for i in range(round(minutes)):
                    xp += int(random.randint(10,21))
                cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{member.guild.id}' and user_id = '{user.id}'")
                result1 = cursor.fetchone()
                exp = int(result1[1])
                sql = ("UPDATE glevel SET exp = ? WHERE guild_id = ? and user_id = ?")
                val = (int(exp + xp), str(member.guild.id), str(user.id))
                cursor.execute(sql, val)
                main.commit()
                xp_start = int(result1[1])
                lvl_start = int(result1[2])
                
                xp_end = math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)
                if xp_end < xp_start:
                    sql = ("UPDATE glevel SET level = ? WHERE guild_id = ? and user_id = ?")
                    val = (int(lvl_start + 1), str(member.guild.id), str(user.id))
                    cursor.execute(sql, val)
                    main.commit()
                    sql1 = ("UPDATE glevel SET exp = ? WHERE guild_id = ? and user_id = ?")
                    val1 = (xp_start-xp_end, str(member.guild.id), str(user.id))  
                    cursor.execute(sql1, val1)
                    main.commit()

                sql = ("UPDATE vlevel SET start_time = ? WHERE guild_id = ? and user_id = ?")
                val = ('none', str(member.guild.id), str(user.id))
                cursor.execute(sql, val)
                main.commit()
                cursor.close()
                main.close()
                VoiceLeveling(self).ranking(member, user)
            elif user in members:
                if sum(1 for m in members if not m.bot) >= 2:
                    return
                else:
                    sql = ("UPDATE vlevel SET start_time = ? WHERE guild_id = ? and user_id = ?")
                    val = ('none', str(member.guild.id), str(user.id))
                    cursor.execute(sql, val)
                    main.commit()
                    cursor.close()
                    main.close()
            else:
                continue
        

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        main = sqlite3.connect('resources/main.db')
        cursor = main.cursor()
        if after.channel is None:
          cursor.close()
          main.close()
          await VoiceLeveling(self).stop_time(member, before, after)
        else:
          cursor.execute(f"SELECT user_id FROM glevel WHERE guild_id = '{member.guild.id}' and user_id = '{member.id}'")
          result = cursor.fetchone()
          if result is None:
            sql = ("INSERT INTO glevel(guild_id, user_id, exp, level) VALUES(?,?,?,?)")
            val = (str(member.guild.id), str(member.id), 0, 0)
            cursor.execute(sql, val)
            main.commit()
            now = datetime.datetime.utcnow()
            sql = ("INSERT INTO vlevel(guild_id, user_id, join_time, channel_id) VALUES(?,?,?,?)")
            val = (str(member.guild.id), str(member.id), now, str(after.channel.id))
            cursor.execute(sql, val)
            main.commit()
            cursor.close()
            main.close()
            await VoiceLeveling(self).start_time(member, before, after)
          else:
            cursor.execute(f"SELECT user_id FROM vlevel WHERE guild_id = '{member.guild.id}' and user_id = '{member.id}'")
            result = cursor.fetchone()
            if result is None:
              now = datetime.datetime.utcnow()
              sql = ("INSERT INTO vlevel(guild_id, user_id, join_time, channel_id) VALUES(?,?,?,?)")
              val = (str(member.guild.id), str(member.id), now, str(after.channel.id))
              cursor.execute(sql, val)
              main.commit()
              cursor.close()
              main.close()
            else:
              now = datetime.datetime.utcnow()
              sql = ("UPDATE vlevel SET join_time = ? and channel_id = ? WHERE guild_id = ? and user_id = ?")
              val = (now, str(after.channel.id), str(member.guild.id), str(member.id))
              cursor.execute(sql, val)
              main.commit()
              cursor.close()
              main.close()
              await VoiceLeveling(self).start_time(member, before, after)

class LevelCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True,aliases=["level","lvl"])
    async def rank(self, ctx, user:discord.User=None):
        if user is None:
            main = sqlite3.connect('resources/main.db')
            cursor = main.cursor()
            cursor.execute(f"SELECT exp, level FROM glevel WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.message.author.id}'")
            result = cursor.fetchone()
            if result is None:
                img = Image.open("resources/rank.png") #Replace infoimgimg.png with your background image.
                draw = ImageDraw.Draw(img)
                font1 = ImageFont.truetype("resources/mcfont.otf", 40) #Make sure you insert a valid font from your folder.
                #    (x,y)::↓ ↓ ↓ (text)::↓ ↓     (r,g,b)::↓ ↓ ↓
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(ctx.author.avatar_url)) as response:
                        image = await response.read()
                icon = Image.open(BytesIO(image)).convert("RGBA")
                img.paste(icon.resize((176, 176)), (32, 32))

                draw.text((880, 36), f"0", (255, 255, 255), font=font1)
                draw.text((880, 100), f"0", (255, 255, 255), font=font1)
                draw.text((880, 164), f"wip", (255, 255, 255), font=font1)
                draw.text((240,36), f"{ctx.author}", (255, 255, 255), font=font1)
                img.save('resources/latest.png') #Change Leveling/infoimg2.png if needed.
                ffile = discord.File("resources/latest.png")
                await ctx.send(file=ffile)
            elif result is not None:
                img = Image.open("resources/rank.png") #Replace infoimgimg.png with your background image.
                draw = ImageDraw.Draw(img)
                font1 = ImageFont.truetype("resources/mcfont.otf", 40)
                lvl_start = (5 * (int(result[1]) ^ 2) + 50 * int(result[1]) + 100)
                progress = math.floor(int(result[0]) / lvl_start * 992)
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(ctx.author.avatar_url)) as response:
                        image = await response.read()
                icon = Image.open(BytesIO(image)).convert("RGBA")
                img.paste(icon.resize((176, 176)), (32, 32))

                draw.text((880, 36), f"{str(result[1])}", (255, 255, 255), font=font1)
                draw.text((880, 100), f"{str(result[0])}", (255, 255, 255), font=font1)
                draw.text((880, 164), f"wip", (255, 255, 255), font=font1)
                draw.text((240,36), f"{ctx.author}", (255, 255, 255), font=font1)
                if progress != 0:
                  draw.rectangle([32, 240, progress, 304], fill=(255,99,183))
                img.save('resources/latest.png') #Change Leveling/infoimg2.png if needed.
                ffile = discord.File("resources/latest.png")
                await ctx.send(file=ffile)
            cursor.close()
            main.close()
        else:
            main = sqlite3.connect('resources/main.db')
            cursor = main.cursor()
            cursor.execute(f"SELECT exp, level FROM glevel WHERE guild_id = '{ctx.guild.id}' and user_id = '{user.id}'")
            result = cursor.fetchone()
            if result is None:
                img = Image.open("resources/rank.png") #Replace infoimgimg.png with your background image.
                draw = ImageDraw.Draw(img)
                font1 = ImageFont.truetype("resources/mcfont.otf", 40) #Make sure you insert a valid font from your folder.
                #    (x,y)::↓ ↓ ↓ (text)::↓ ↓     (r,g,b)::↓ ↓ ↓
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(user.avatar_url)) as response:
                        image = await response.read()
                icon = Image.open(BytesIO(image)).convert("RGBA")
                img.paste(icon.resize((176, 176)), (32, 32))

                draw.text((880, 36), f"0", (255, 255, 255), font=font1)
                draw.text((880, 100), f"0", (255, 255, 255), font=font1)
                draw.text((880, 164), f"wip", (255, 255, 255), font=font1)
                draw.text((240,36), f"{user.name}#{user.discriminator}", (255, 255, 255), font=font1)
                img.save('resources/latest.png') #Change Leveling/infoimg2.png if needed.
                ffile = discord.File("resources/latest.png")
                await ctx.send(file=ffile)
            elif result is not None:
                img = Image.open("resources/rank.png") #Replace infoimgimg.png with your background image.
                draw = ImageDraw.Draw(img)
                font1 = ImageFont.truetype("resources/mcfont.otf", 35)
                lvl_start = (5 * (int(result[1]) ^ 2) + 50 * int(result[1]) + 100)
                progress = math.floor(int(result[0]) / lvl_start * 992)
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(user.avatar_url)) as response:
                        image = await response.read()
                icon = Image.open(BytesIO(image)).convert("RGBA")
                img.paste(icon.resize((176, 176)), (32, 32))

                draw.text((880, 36), f"{str(result[1])}", (255, 255, 255), font=font1)
                draw.text((880, 100), f"{str(result[0])}", (255, 255, 255), font=font1)
                draw.text((880, 164), f"wip", (255, 255, 255), font=font1)
                draw.text((240,36), f"{user.name}#{user.discriminator}", (255, 255, 255), font=font1)
                if progress != 0:
                  draw.rectangle([32, 240, progress, 304], fill=(255,99,183))
                img.save('resources/latest.png') #Change Leveling/infoimg2.png if needed.
                ffile = discord.File("resources/latest.png")
                await ctx.send(file=ffile)
            cursor.close()
            main.close()

    @commands.command(pass_context=True, aliases=["lb"])
    async def leaderboard(self, ctx):
        main = sqlite3.connect('resources/main.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{ctx.guild.id}' ORDER BY level DESC, exp DESC")
        result = cursor.fetchall()
        desc = ''
        v = 1
        for result in result:
          if v > 5:
            break
            
          if result[0] == None:
            continue
            
          user = self.bot.get_user(int(result[0]))
          lvl = result[2]
          exp = result[1]
          desc+=f'\n{str(user)}'+f'\n- level **{lvl}**, **{exp}** exp'
          v += 1
        if desc == "":
          desc = "No one's ranked yet :("
            
        LeaderboardE = discord.Embed(
          colour=0xff63b7,
          title=f"Leaderboard **»** levels",
          description=f"{desc}"
        )
        LeaderboardE.set_thumbnail(url=self.bot.thumbnail)
        LeaderboardE.set_footer(text=f"Made by llama • Requested by {ctx.author.name}", icon_url=str(ctx.author.avatar_url_as(static_format='png', size=2048)))
        await ctx.send(embed=LeaderboardE)


def setup(bot):
    try:
        bot.add_cog(LevelCommands(bot))
        print(f'{Fore.GREEN}Loaded "levelcommands" cog!')
    except Exception as e:
        print(f'{Fore.RED}Error while adding cog "levelcommands"', e)
    try:
        bot.add_cog(TextLeveling(bot))
        print(f'{Fore.GREEN}Loaded "textleveling" cog!')
    except Exception as e:
        print(f'{Fore.RED}Error while adding cog "textleveling"', e)
    try:
        bot.add_cog(VoiceLeveling(bot))
        print(f'{Fore.GREEN}Loaded "voiceleveling" cog!')
    except Exception as e:
        print(f'{Fore.RED}Error while adding cog "voiceleveling"', e)
    try:
        bot.add_cog(Ranks(bot))
        print(f'{Fore.GREEN}Loaded "ranks" cog!')
    except Exception as e:
        print(f'{Fore.RED}Error while adding cog "ranks"', e)