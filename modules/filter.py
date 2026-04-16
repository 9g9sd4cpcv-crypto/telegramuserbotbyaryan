from pyrogram import filters
from better_profanity import profanity

profanity.load_censor_words()

def init(app):

    @app.on_message(filters.text & filters.group)
    async def bad(_, m):
        if profanity.contains_profanity(m.text):
            await m.delete()
