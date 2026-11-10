import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN belum diatur!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🎬 KATALOG FILM", callback_data="catalog"),
        InlineKeyboardButton("📺 CHANNEL GRATIS", callback_data="free"),
        InlineKeyboardButton("⭐ ARFLIX PREMIUM", callback_data="premium"),
        InlineKeyboardButton("ℹ️ BANTUAN", callback_data="help")
    )

    bot.send_message(
        message.chat.id,
        "🎬 SELAMAT DATANG DI ARFLIX\n\n"
        "Tempat menemukan rekomendasi dan katalog film.\n\n"
        "Silakan pilih menu di bawah ini:",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: True)
def menu(call):
    if call.data == "catalog":
        text = (
            "🎬 KATALOG ARFLIX\n\n"
            "Katalog film akan segera tersedia.\n"
            "Kami hanya menyediakan tautan tontonan resmi "
            "dan konten yang memiliki izin distribusi."
        )
    elif call.data == "free":
        text = "📺 CHANNEL GRATIS\n\nLink channel akan ditambahkan nanti."
    elif call.data == "premium":
        text = "⭐ ARFLIX PREMIUM\n\nFitur premium sedang dipersiapkan."
    elif call.data == "help":
        text = "ℹ️ BANTUAN\n\nKetik /start untuk membuka menu utama."
    else:
        text = "Menu tidak ditemukan."

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text)

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "Bantuan ARFlix Bot\n\n"
        "/start - Membuka menu utama\n"
        "/help - Bantuan"
    )

print("ARFlix Bot sedang berjalan...")
bot.infinity_polling()
