from pyrogram import filters
from modules.db import users

def init(app):

    @app.on_message(filters.group)
    async def track(_, m):
        await users.update_one(
            {"user": m.from_user.id},
            {"$inc": {"messages": 1}},
            upsert=True
        )

    @app.on_message(filters.command("top", "."))
    async def top(_, m):
        cursor = users.find().sort("messages", -1).limit(10)
        text = "🏆 Top Users:\n"

        i = 1
        async for u in cursor:
            text += f"{i}. {u['user']} → {u['messages']}\n"
            i += 1

        await m.reply(text)
