from pyrogram import filters
from modules.db import groups

def init(app):

    @app.on_message(filters.command("welcomeon", "."))
    async def on(_, m):
        await groups.update_one(
            {"chat": m.chat.id},
            {"$set": {"welcome": True}},
            upsert=True
        )
        await m.reply("✅ Welcome ON")

    @app.on_message(filters.new_chat_members)
    async def welcome(_, m):
        data = await groups.find_one({"chat": m.chat.id})

        if data and data.get("welcome"):
            for user in m.new_chat_members:
                await m.reply(f"Welcome {user.mention} 🎉")
