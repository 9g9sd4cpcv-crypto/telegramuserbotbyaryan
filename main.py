from pyrogram import Client, filters
from config import *

# IMPORT ALL MODULES PROPERLY
from modules import admin, ranks, activity, filter, profile, music, logger, welcome


# ---------------- CLIENT ----------------
app = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION
)


# ---------------- BASIC COMMANDS ----------------
@app.on_message(filters.command("alive", "."))
async def alive(_, m):
    await m.reply("🔥 Userbot is Alive")


@app.on_message(filters.command("ping", "."))
async def ping(_, m):
    await m.reply("🏓 Pong")


# ---------------- LOAD MODULES ----------------
admin.init(app)
ranks.init(app)
activity.init(app)
filter.init(app)
profile.init(app)
music.init(app)
logger.init(app)
welcome.init(app)


# ---------------- START BOT ----------------
print("🚀 Userbot Starting...")
app.run()
