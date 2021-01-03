from discord.ext import commands
from colorama import Fore, init
import traceback
import discord
import datetime
import typing
import re


class Steal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_emojis=True)
    @commands.bot_has_permissions(manage_emojis=True)
    async def steal(self, ctx, emoji: typing.Union[discord.PartialEmoji, int, str]):
        if isinstance(emoji, discord.PartialEmoji):
            try:
                raw = await emoji.url.read()
            except discord.HTTPException as e:
                return await ctx.error(f"Failed to fetch image ({e.status})")
            try:
                stolen = await ctx.guild.create_custom_emoji(
                    name=emoji.name, image=raw, reason=f"Stolen by {ctx.author}"
                )
            except discord.DiscordException as e:
                return await ctx.send(f"Failed to create the emote")
            return await ctx.send(f"Successfully stole emote {stolen}")
        elif isinstance(emoji, int):
            asset = discord.Asset(self.bot._connection, f"/emojis/{emoji}")
            try:
                raw = await asset.read()
            except discord.HTTPException as e:
                return await ctx.send(
                    f"Failed to fetch image, make sure the id is a valid emote id ({e.status})"
                )
            stolen = await ctx.guild.create_custom_emoji(
                name="stolen_emoji", image=raw, reason=f"Stolen by {ctx.author}"
            )
            return await ctx.send(
                f"Successfully stole emoji {stolen} (you might wanna rename it)"
            )
        elif isinstance(emoji, str):
            try:
                asset_url = (
                    re.findall(
                        r"https?:\/\/cdn\.discordapp\.com(\/emojis\/\d{15,21})\.\w{3,4}",
                        emoji,
                        re.MULTILINE,
                    )
                )[
                    0
                ]
            except IndexError:
                return await ctx.send("you must provide a valid emoji id")
            asset = discord.Asset(self.bot._connection, asset_url)
            try:
                raw = await asset.read()
            except discord.HTTPException as e:
                return await ctx.error(
                    f"Failed to fetch image, make sure the url is a valid emote url ({e.status})"
                )
            stolen = await ctx.guild.create_custom_emoji(
                name="stolen_emoji", image=raw, reason=f"Stolen by {ctx.author}"
            )
            return await ctx.send(
                f"Successfully stole emoji {stolen} (you might wanna rename it)"
            )


def setup(bot):
    try:
        bot.add_cog(Steal(bot))
        print(f'{Fore.GREEN}Loaded steal command!')
    except Exception as e:
        print(f'{Fore.RED}Error while adding command steal', e)