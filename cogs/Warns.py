import discord, random, os, json
from discord.ext import commands
from setup import var
from functions import customerror
from functions import functions
from datetime import datetime

class Warns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="warn", description="[member] *[reason]|Warn a member", aliases=["strike"])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason = "None"):
        data = await functions.read_data("databases/warns.json")

        thedate = str(datetime.now())
        if str(ctx.guild.id) not in data:
            data[str(ctx.guild.id)] = {}
        if str(member.id) not in data[str(ctx.guild.id)]:
            data[str(ctx.guild.id)][str(member.id)] = {
                "1":{
                    "time":thedate,
                    "mod":str(ctx.author.id),
                    "reason":reason
                }
            }
        else:
            data[str(ctx.guild.id)][str(member.id)][str(len(data[str(ctx.guild.id)][str(member.id)]) + 1)] = {
                "time":thedate,
                "mod":str(ctx.author.id),
                "reason":reason
            }
        
        data = await functions.save_data("databases/warns.json", data)

        try:
            await ctx.message.delete()
        except:
            pass

        what = await functions.check_events(self.bot, data, ctx.guild, member)
        noArg = f"\n\n__Top tip!__ Add a warn reason with `{functions.prefix(ctx.guild)}warn [user] [reason]`!"

        try:
            memberEmbed = discord.Embed(
                title=random.choice(["Uh oh!", "Oops!", "Oh no!"]),
                description=f"You have been warned in **{ctx.guild.name}** for: **{reason}**" + (f". You were also given a **{what}** automatically." if what != None else ""),
                color=var.embedFail
            )
            await member.send(embed=memberEmbed)
            embed = discord.Embed(
                title=random.choice([f"Successfully warned {member.display_name}", "Successfully warned!", f"Warned {member.display_name} successfully!"]),
                description=f"Warned **{member.display_name}** successfully with reason: **{reason}**" + (f". They were also given a **{what}** due to your [Server Events]({var.address}/dashboard#{ctx.guild.id})" if what != None else "") + (noArg if reason == "None" else ""),
                colour=var.embedSuccess
            )
        except:
            embed = discord.Embed(
                title=random.choice([f"Successfully warned {member.display_name}", "Successfully warned!", f"Warned {member.display_name} successfully!"]),
                description=f"Warned **{member.display_name}** successfully with reason: **{reason}**, however could not DM them." + (f". They were also given a **{what}** due to your [Server Events]({var.address}/dashboard#{ctx.guild.id})" if what != None else "") + (noArg if reason == "None" else ""),
                colour=var.embedSuccess
            )
        embed.add_field(name="Warn ID", value=len(data[str(ctx.guild.id)][str(member.id)]))
        embed.add_field(name="Moderator", value=str(ctx.author))
        embed.set_footer(text=f"{member.display_name} now has {len(data[str(ctx.guild.id)][str(member.id)])} warn(s)")
        await ctx.send(embed=embed)
    
    @commands.command(name="warns", description="*[member]|Check a users warns", aliases=['viewwarns', 'viewwarn', 'mywarns', 'mywarn'])
    @commands.guild_only()
    async def warns(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        data = await functions.read_data("databases/warns.json")
        embedNone = discord.Embed(
            title=random.choice([f"Found no warns for {member.display_name}", f"{member.display_name} has no warns"]),
            description=f"Could not find any warns for **{member.display_name}** :tada:", 
            colour=var.embed
        )
        if str(ctx.guild.id) not in data:
            return await ctx.send(embed=embedNone)
        elif str(member.id) not in data[str(ctx.guild.id)]:
            return await ctx.send(embed=embedNone)
        for warn in data[str(ctx.guild.id)][str(member.id)]:
            embed = discord.Embed(
                title=random.choice([f"Found warns for {member.display_name}", f"{member.display_name}'s warns"]),
                description=f"Here {'is' if len(data[str(ctx.guild.id)][str(member.id)]) == 1 else 'are'} the **{len(data[str(ctx.guild.id)][str(member.id)])}** warn{'' if len(data[str(ctx.guild.id)][str(member.id)]) == 1 else 's'} I found for **{member.display_name}**", 
                colour=var.embed
            )

            f_date = datetime.strptime(data[str(ctx.guild.id)][str(member.id)][warn]['time'], '%Y-%m-%d %H:%M:%S.%f')
            l_date = datetime.now()
            delta = l_date - f_date

            embed.add_field(
                name=f"ID: {warn} - Moderator: {self.bot.get_user(int(data[str(ctx.guild.id)][str(member.id)][warn]['mod']))} - {str(delta.days)} day{'' if delta.days == 1 else 's'} ago", 
                value=data[str(ctx.guild.id)][str(member.id)][warn]["reason"], 
                inline=False
            )
        return await ctx.send(embed=embed)
    
    @commands.command(name="delwarn", description="[member] [warnID/all]|Check a users warns", aliases=['del-warn', 'deletewarn', 'del-warns', 'deletewarns', 
        'delete-warns', 'delete-warn', 'delwarns', 'remove-warn', 'remove-warns', 'removewarn', 'removewarns'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def delwarn(self, ctx, member: discord.Member, *, warnid):
        data = await functions.read_data("databases/warns.json")
        embedNone = discord.Embed(
            title=random.choice([f"Found no warns for {member.display_name}", f"{member.display_name} has no warns"]),
            description=f"Could not find any warns for **{member.display_name}**", 
            colour=var.embedFail
        )
        embedNo = discord.Embed(
            title=random.choice([f"Could not find warn ID {warnid}", f"Could not find a warn with ID {warnid}"]),
            description=f"Could not find any warns for **{member.display_name}** with warn ID **{warnid}**", 
            colour=var.embedFail
        )
        embedAll = discord.Embed(
            title=random.choice([f"Deleted all warns for {member.display_name}", f"Deleted all of {member.display_name}'s warns"]),
            description=f"Deleted all warns for **{member.display_name}**", 
            colour=var.embedSuccess
        )
        embed = discord.Embed(
            title=random.choice([f"Deleted warn ID **{warnid}**", f"Deleted {member.display_name}'s warn"]),
            description=f"Deleted warn with ID **{warnid}** for **{member.display_name}**", 
            colour=var.embedSuccess
        )
        if str(ctx.guild.id) not in data:
            return await ctx.send(embed=embedNone)
        elif str(member.id) not in data[str(ctx.guild.id)]:
            return await ctx.send(embed=embedNone)
        elif warnid == "all":
            wrns = []
            for warn in data[str(ctx.guild.id)][str(member.id)]:
                wrns.append(warn)
            for warn in wrns:
                del data[str(ctx.guild.id)][str(member.id)][warn]
            await ctx.send(embed=embedAll)
        elif warnid not in data[str(ctx.guild.id)][str(member.id)]:
            return await ctx.send(embed=embedNo)
        else:
            del data[str(ctx.guild.id)][str(member.id)][warnid]
            await ctx.send(embed=embed)

        if len(data[str(ctx.guild.id)][str(member.id)]) == 0:
            del data[str(ctx.guild.id)][str(member.id)]
        if len(data[str(ctx.guild.id)]) == 0:
            del data[str(ctx.guild.id)]

        await functions.save_data("databases/warns.json", data)

def setup(bot):
    bot.add_cog(Warns(bot))