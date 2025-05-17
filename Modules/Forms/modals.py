import discord
from discord.ui import Modal, TextInput
from Modules.Forms.database import cursor, conn
from Config.Forms.config import *
import json

class FormModal(Modal):
    def __init__(self, form_data):
        super().__init__(title=form_data["title"])
        self.form_data = form_data
        self.responses = {}

        for question in form_data["questions"]:
            if question["type"] == "text":
                self.add_item(
                    TextInput(
                        label=question["label"],
                        placeholder=question.get("placeholder", ""),
                        required=True
                    )
                )

    async def on_submit(self, interaction: discord.Interaction):
        for child in self.children:
            if isinstance(child, TextInput):
                self.responses[child.label] = child.value

        cursor.execute(
            "INSERT INTO forms (creator_id, created_at, responses) VALUES (?, datetime('now'), ?)",
            (interaction.user.id, json.dumps(self.responses))
        )
        conn.commit()

        response_message = "\n".join([f"{key}: {value}" for key, value in self.responses.items()])

        log_channel_id = SETTINGS["log_channel_id"]
        log_channel = interaction.guild.get_channel(log_channel_id)
        if log_channel:
            embed = discord.Embed(
                title=loc["log_embed_title"],
                color=discord.Color(SETTINGS["log_embed_color"])
            )
            embed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
            for key, value in self.responses.items():
                embed.add_field(name=key, value=value, inline=False)


            await log_channel.send(embed=embed)
            

        await interaction.response.send_message(loc["messages"]["modal_response"].format(response_message), ephemeral=True)
