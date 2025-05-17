import discord
from discord.ext import commands, tasks
import asyncio
import random
import json
from datetime import datetime, timedelta
from Config.Giveaway.config import *

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaways = []
        self.DATA_FILE = save_path
        self.load_giveaways()
        self.check_giveaways.start()

    def save_giveaways(self):
        with open(self.DATA_FILE, "w") as f:
            json.dump(self.giveaways, f, default=str)

    def load_giveaways(self):
        try:
            with open(self.DATA_FILE, "r") as f:
                self.giveaways = json.load(f)
                for g in self.giveaways:
                    g["end_time"] = datetime.fromisoformat(g["end_time"])
        except FileNotFoundError:
            self.giveaways = []
    
    

    @commands.command()
    @commands.has_role(command_role)
    async def giveaway(self, ctx, end_time: str, *, prize: str):
        try:
            end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
            if end_time <= datetime.now():
                await ctx.send(loc["error"]["no_date"])
                return
        except ValueError:
            await ctx.send(loc["error"]["incorrect_date_format"])
            return
        
        embed = discord.Embed(title=loc["embed"]["giveaway_title"], description=loc["embed"]["giveaway_description"].format(prize), color=discord.Color.gold())
        embed.set_footer(text=loc["embed"]["giveaway_footer"].format(end_time))
        message = await ctx.send(embed=embed)
        await message.add_reaction("🎉")
        
        self.giveaways.append({"message_id": message.id, "channel_id": ctx.channel.id, "end_time": end_time.isoformat(), "prize": prize})
        self.save_giveaways()

    @tasks.loop(seconds=60)
    async def check_giveaways(self):
        now = datetime.now()
        remaining = []
        for g in self.giveaways:
            if isinstance(g["end_time"], str): g["end_time"] = datetime.fromisoformat(g["end_time"])
            if g["end_time"] <= now:
                channel = self.bot.get_channel(g["channel_id"])
                if channel:
                    try:
                        message = await channel.fetch_message(g["message_id"])
                        users = [user async for user in message.reactions[0].users() if not user.bot]
                        if users:
                            winner = random.choice(users)
                            await channel.send(loc["messages"]["сongratulations_in_the_general_channel"].format(winner.mention, g["prize"]))
                            await winner.send(loc["messages"]["congratulations_in_private_messages"].format(winner.mention, g["prize"]))
                        else: await channel.send(loc["messages"]["not_enough_participants"])
                    except discord.NotFound: pass
            else: remaining.append(g)
        self.giveaways = remaining
        self.save_giveaways()

async def setup(bot):
    await bot.add_cog(Giveaway(bot))
