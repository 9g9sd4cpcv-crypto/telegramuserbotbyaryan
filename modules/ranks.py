from pyrogram import filters
from modules.db import ranks
from config import OWNER_ID

async def get_rank(user_id):
    u = await ranks.find_one({"user_id": user_id})
    return u["rank"] if u else "member"

async def set_rank(user_id, rank):
    await ranks.update_one(
        {"user_id": user_id},
        {"$set": {"rank": rank}},
        upsert=True
    )

def init(app):

    @app.on_message(filters.command("addowner", "."))
    async def add_owner(_, m):
        if m.from_user.id != OWNER_ID:
            return
        user = m.reply_to_message.from_user.id
        await set_rank(user, "owner")
        await m.reply("✅ Co-owner added")

    @app.on_message(filters.command("addadmin", "."))
    async def add_admin(_, m):
        user = m.reply_to_message.from_user.id
        await set_rank(user, "admin")
        await m.reply("✅ Admin added")

    @app.on_message(filters.command("myrank", "."))
    async def myrank(_, m):
        rank = await get_rank(m.from_user.id)
        await m.reply(f"🎖 Rank: {rank}")
