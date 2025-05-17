import discord
from discord.ext import commands
from Modules.Tools.main import *


class NewMembers(commands.Cog):
    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Welcome {member.mention} to {guild.name}!'
            await Tools.respond(guild.system_channel, to_send)
            await guild.system_channel.send(to_send)

async def setup(bot):
    cog = NewMembers(bot)
    await bot.add_cog(cog)