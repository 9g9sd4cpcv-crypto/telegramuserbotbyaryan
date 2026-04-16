from pyrogram import filters

def init(app):

    @app.on_message(filters.command("clone", "."))
    async def clone(client, m):
        user = m.reply_to_message.from_user

        photos = []
        async for p in client.get_chat_photos(user.id):
            photos.append(p.file_id)
            break

        if photos:
            await client.set_profile_photo(photo=photos[0])

        await client.update_profile(
            first_name=user.first_name,
            bio=user.bio or ""
        )

        await m.reply("✅ Cloned")
