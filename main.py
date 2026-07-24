  import os
import threading
from flask import Flask
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

nest_asyncio.apply()

# --- MINI WEB SERVER UNTUK RENDER FREE ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Muz AI OS Server is Running Live 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- BOT TELEGRAM KAU ---
TOKEN = "8972960445:AAG43M7W-pE-l-r6fS5r8S9T1_V6N-mE8xY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    text = (
        f"Salam & Hello {user_name}! 👋\n\n"
        f"Aku ialah **Muz AI OS** — Asisten AI peribadi kau.\n"
        f"Server Render 24/7 dah *LIVE* & percuma! 🚀\n\n"
        f"Taip apa-apa mesej untuk borak dengan aku."
    )
    await update.message.reply_text(text, parse_mode='Markdown')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    reply = f"🤖 **Muz AI OS:** Kau kata -> '{user_msg}'\n\n*(Sistem AI penuh bakal dimasukkan tak lama lagi!)*"
    await update.message.reply_text(reply, parse_mode='Markdown')

if __name__ == '__main__':
    # Jalan web server kat background
    threading.Thread(target=run_web, daemon=True).start()
    
    # Jalan Telegram Bot
    print("Muz AI OS Server sedang berjalan...")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    app.run_polling()
    
