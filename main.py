from pyrogram import Client, filters
from config import *

# IMPORTANT: correct import style
from modules.admin import init as admin_init
from modules.ranks import init as ranks_init
from modules.activity import init as activity_init
from modules.filter import init as filter_init
from modules.profile import init as profile_init
from modules.music import init as music_init
from modules.logger import init as logger_init
from modules.welcome import init as welcome_init


app = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION
)


@app.on_message(filters.command("alive", "."))
async def alive(_, m):
    await m.reply("🔥 Alive")


@app.on_message(filters.command("ping", "."))
async def ping(_, m):
    await m.reply("🏓 Pong")


# LOAD MODULES (SAFE METHOD)
admin_init(app)
ranks_init(app)
activity_init(app)
filter_init(app)
profile_init(app)
music_init(app)
logger_init(app)
welcome_init(app)


print("🚀 Bot Started")
app.run()
