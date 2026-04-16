from pyrogram import filters

logs = []

def init(app):

    @app.on_message()
    async def log(_, m):
        if m.text:
            logs.append(m.text)

    @app.on_message(filters.command("logs", "."))
    async def show(_, m):
        await m.reply("\n".join(logs[-20:]) or "No logs")
