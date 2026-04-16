from pyrogram import filters
from modules.db import warns

MAX_WARN = 3

def init(app):

    @app.on_message(filters.command("warn", "."))
    async def warn(_, m):
        user = m.reply_to_message.from_user.id

        data = await warns.find_one({"user": user}) or {"count": 0}
        count = data["count"] + 1

        await warns.update_one(
            {"user": user},
            {"$set": {"count": count}},
            upsert=True
        )

        if count >= MAX_WARN:
            await m.chat.ban_member(user)
            await m.reply("🚫 Banned (3 warns)")
        else:
            await m.reply(f"⚠️ Warn {count}/3")

    @app.on_message(filters.command("unbanall", "."))
    async def unbanall(_, m):
        async for member in m.chat.get_members():
            try:
                await m.chat.unban_member(member.user.id)
            except:
                pass
        await m.reply("✅ Unbanned all")
