from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
import yt_dlp

vc = None
queues = {}
loop = {}

# ---------- YT SEARCH ----------
def yt_search(query):
    ydl_opts = {
        "format": "bestaudio",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
        return info["url"], info["title"]

# ---------- BUTTONS ----------
def buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⏸ Pause", callback_data="pause"),
            InlineKeyboardButton("▶️ Resume", callback_data="resume"),
        ],
        [
            InlineKeyboardButton("⏭ Skip", callback_data="skip"),
            InlineKeyboardButton("⏹ Stop", callback_data="stop"),
        ],
        [
            InlineKeyboardButton("🔁 Loop", callback_data="loop"),
        ]
    ])

# ---------- PLAY NEXT ----------
async def play_next(chat_id):
    if chat_id not in queues or not queues[chat_id]:
        await vc.leave_group_call(chat_id)
        return

    if loop.get(chat_id):
        url, title = queues[chat_id][0]
    else:
        url, title = queues[chat_id].pop(0)

    await vc.change_stream(
        chat_id,
        AudioPiped(url, HighQualityAudio())
    )

# ---------- INIT ----------
def init(app):
    global vc
    vc = PyTgCalls(app)

    # ▶ PLAY
    @app.on_message(filters.command("play", ".") & filters.group)
    async def play(_, m):
        if len(m.command) < 2:
            return await m.reply("Usage: .play song name")

        query = m.text.split(None, 1)[1]

        msg = await m.reply("🔍 Searching...")

        url, title = yt_search(query)

        if m.chat.id not in queues:
            queues[m.chat.id] = []

        queues[m.chat.id].append((url, title))

        try:
            await vc.join_group_call(
                m.chat.id,
                AudioPiped(url, HighQualityAudio())
            )

            await msg.edit(
                f"🎵 Now Playing:\n{title}",
                reply_markup=buttons()
            )

        except:
            await msg.edit(f"➕ Added to queue:\n{title}")

    # 🎛 CONTROLS
    @app.on_callback_query()
    async def controls(_, cq):
        chat_id = cq.message.chat.id

        if cq.data == "pause":
            await vc.pause_stream(chat_id)
            await cq.answer("Paused")

        elif cq.data == "resume":
            await vc.resume_stream(chat_id)
            await cq.answer("Resumed")

        elif cq.data == "skip":
            await play_next(chat_id)
            await cq.answer("Skipped")

        elif cq.data == "stop":
            queues[chat_id] = []
            await vc.leave_group_call(chat_id)
            await cq.answer("Stopped")

        elif cq.data == "loop":
            loop[chat_id] = not loop.get(chat_id, False)
            await cq.answer(f"Loop: {loop[chat_id]}")

    # 📜 SHOW QUEUE
    @app.on_message(filters.command("queue", "."))
    async def show_queue(_, m):
        if m.chat.id not in queues or not queues[m.chat.id]:
            return await m.reply("Empty queue")

        text = "📜 Queue:\n"
        for i, (_, title) in enumerate(queues[m.chat.id][:10], 1):
            text += f"{i}. {title}\n"

        await m.reply(text)

    # 🔊 AUTO NEXT
    @vc.on_stream_end()
    async def stream_end(_, update):
        await play_next(update.chat_id)

    vc.start()
