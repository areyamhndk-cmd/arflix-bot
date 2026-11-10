
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN belum diatur!")

bot = telebot.TeleBot(TOKEN)

GENRES = [
    ("👻 HOROR", "horror"),
    ("😂 KOMEDI", "comedy"),
    ("💥 AKSI", "action"),
    ("❤️ ROMANTIS", "romance"),
    ("🔪 THRILLER", "thriller"),
    ("🚀 SCI-FI", "scifi"),
    ("🐉 FANTASI", "fantasy"),
    ("🎨 ANIMASI", "animation"),
]

def menu_utama():
    kb = InlineKeyboardMarkup(row_width=2)
    for nama, kode in GENRES:
        kb.add(InlineKeyboardButton(nama, callback_data="genre_" + kode))
    kb.add(InlineKeyboardButton("🎞️ DEMO PEMUTAR VIDEO", callback_data="demo"))
    kb.add(InlineKeyboardButton("📺 CHANNEL GRATIS", callback_data="free"))
    kb.add(InlineKeyboardButton("⭐ ARFLIX PREMIUM", callback_data="premium"))
    return kb

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🎬 SELAMAT DATANG DI ARFLIX\n\n"
        "Pilih genre film atau coba demo pemutar video.",
        reply_markup=menu_utama()
    )

@bot.callback_query_handler(func=lambda call: True)
def tombol(call):
    bot.answer_callback_query(call.id)

    if call.data == "demo":
        bot.send_message(
            call.message.chat.id,
            "🎞️ DEMO PEMUTAR ARFLIX\n\n"
            "Kirim video milik sendiri atau video yang kamu punya izin untuk bagikan.\n"
            "Bot akan mengirimkannya kembali agar bisa diputar langsung di Telegram."
        )

    elif call.data.startswith("genre_"):
        genre = call.data.replace("genre_", "").upper()
        bot.send_message(
            call.message.chat.id,
            f"🎬 KATALOG {genre}\n\n"
            "Daftar film sedang disiapkan. "
            "Katalog hanya akan berisi video yang memiliki izin tayang."
        )

    elif call.data == "free":
        bot.send_message(call.message.chat.id, "📺 CHANNEL GRATIS\nLink akan ditambahkan nanti.")

    elif call.data == "premium":
        bot.send_message(call.message.chat.id, "⭐ ARFLIX PREMIUM\nFitur sedang dipersiapkan.")

@bot.message_handler(content_types=["video"])
def video_demo(message):
    bot.send_video(
        message.chat.id,
        message.video.file_id,
        caption="🎬 ARFLIX VIDEO DEMO"
    )

@bot.message_handler(commands=["help"])
def bantuan(message):
    bot.send_message(message.chat.id, "Ketik /start untuk membuka menu ARFlix.")

print("ARFlix Bot sedang berjalan...")
bot.infinity_polling()
        
