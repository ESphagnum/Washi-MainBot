import json
from config import language

# Insert authors' id in here, user in this set are allowed to use command "runningservers"
authors = (1061998983158964285) # admin

save_path = "Saves/Music"

useEmbed = False
locate = f"Lang/Music/music_{language}.json"
loc = json.load(open(locate,"r",encoding="utf-8"))

# Error messages for returning meaningfull error message to user
error_messages = {
    "ERROR: Sign in to confirm your age\nThis video may be inappropriate for some users.": loc["error"]["age_restriction"],
    "Video unavailable": loc["error"]["unavailable"],
    "ERROR: Private video\nSign in if you've been granted access to this video": loc["error"]["private"]
}

# Commandline options for youtube-dl and ffmpeg
YTDL_OPTIONS_PLAYLIST = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'extract_flat': 'in_playlist',
}
YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}
