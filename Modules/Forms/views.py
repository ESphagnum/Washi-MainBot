from discord.ui import View
from Modules.Forms.buttons import SubmitButton

class FormView(View):
    def __init__(self, form_data):
        super().__init__(timeout=None)
        self.add_item(SubmitButton(form_data))
