import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 1. Masukkan Key & Token korang kat sini (atau guna Environment Variables kat Render)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8972960445:AAGzQuOCOOlDBq13Hb6lTkKc2cbPl8Brl9s") # Masukkan token bot Telegram korang
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "MASUKKAN_GEMINI_API_KEY_KAU_KAT_SINI") # Masukkan Gemini API Key

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Fungsi bila tekan /start kat Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salam bro! Muz AI OS dah sedia online 24/7. Tanyakan apa-apa soalan!")

# Fungsi bila mesej biasa dihantar kat Telegram
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # Hantar soalan pengguna ke Gemini AI
        response = model.generate_content(user_text)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Maaf bro, ada masalah teknikal: {e}"

    # Balas balik mesej kat Telegram
    await update.message.reply_text(bot_reply)

if __name__ == '__main__':
    # Bina aplikasi bot Telegram
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Tambah handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot Muz AI OS sedang berjalan 24/7...")
    app.run_polling()
  
