import json
from config import language

useEmbed = False
locate = f"Lang/Giveaway/giveaway_{language}.json"
loc = json.load(open(locate,"r",encoding="utf-8"))
save_path = "Saves/Giveaway/data.json"

command_role = "🇸​🇪​🇳​🇮​🇴​🇷​ 🇲​🇴​🇩​🇪​🇷​🇦​🇹​🇴​🇷​"