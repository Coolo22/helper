import discord, random, os, json
from discord.ext import commands
from functions import customerror, functions, google
from setup import var
from datetime import datetime, timedelta

class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def cogload(self, ctx, *, cog: str):
        cog = "cogs." + cog.replace("cogs.", "")
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cogunload(self, ctx, *, cog: str):
        cog = "cogs." + cog.replace("cogs.", "")
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def cogreload(self, ctx, *, cog: str):
        cog = "cogs." + cog.replace("cogs.", "")
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')
    

def setup(bot):
    bot.add_cog(Owner(bot))