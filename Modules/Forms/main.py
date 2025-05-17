import discord
from discord.ext import commands
from Modules.Forms.views import FormView
from Modules.Forms.database import save_interactive_message, get_all_interactive_messages, delete_interactive_message
from Modules.Tools.main import *
from Config.Forms.config import *
import json
from importlib import reload

class FormCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def restore_messages(self):
        data = get_all_interactive_messages()
        for message_id, channel_id, msg_type, data in data:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                continue

            try:
                message = await channel.fetch_message(message_id)

                data = json.loads(data)
                if msg_type == "form":
                    view = FormView(data)
                    embed = discord.Embed(
                        title=data["title"],
                        description=data["description"],
                        color=data["embed_color"]
                    )
                    embed.set_image(url=data["image"])
                    await message.edit(embed=embed, view=view)
            except discord.NotFound:
                # Удаляем записи, если сообщение не найдено
                delete_interactive_message(message_id)

    @commands.command()
    @commands.has_role(SETTINGS["command_role"])
    async def form(self, ctx, form_type: str):

        if form_type not in FORMS:
            await Tools.respond(ctx, loc["error"]["form_not_found"].format(form_type), color=0xff0000)
            return

        form_data = FORMS[form_type]
        view = FormView(form_data)
        embed = discord.Embed(
            title=form_data["title"],
            description=form_data["description"],
            color=form_data["embed_color"],
        )
        if form_data["image"] == None: pass
        else: embed.set_image(url=form_data["image"])
        sent_message = await ctx.send(embed=embed, view=view)
        save_interactive_message(sent_message.id, ctx.channel.id, "form", form_data)
    

async def setup(bot):
    cog = FormCog(bot)
    await cog.restore_messages()
    await bot.add_cog(cog)
