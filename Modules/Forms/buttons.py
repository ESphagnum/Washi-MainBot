import discord
from discord.ui import Button
from Modules.Forms.modals import FormModal
from Config.Forms.config import loc

class SubmitButton(Button):
    def __init__(self, form_data):
        super().__init__(label=loc["btn_label"]["form_button"], style=discord.ButtonStyle.danger)
        self.form_data = form_data

    async def callback(self, interaction: discord.Interaction):
        modal = FormModal(self.form_data)
        await interaction.response.send_modal(modal)

