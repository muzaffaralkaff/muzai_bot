import os
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

nest_asyncio.apply()

# Masukkan Token Kau Kat Sini
TOKEN = "8972960445:AAG43M7W-pE-l-r6fS5r8S9T1_V6N-mE8xY"

# Mesej Aluan /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    text = (
        f"Salam & Hello {user_name}! 👋\n\n"
        f"Aku ialah **Muz AI OS** — Asisten AI peribadi kau.\n"
        f"Server 24/7 dah *LIVE* & sedia berkhidmat! 🚀\n\n"
        f"Taip apa-apa mesej untuk borak dengan aku."
    )
    await update.message.reply_text(text, parse_mode='Markdown')

# Chat Echo / Auto Reply
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    reply = f"🤖 **Muz AI OS:** Kau kata -> '{user_msg}'\n\n*(Sistem AI penuh bakal dimasukkan tak lama lagi!)*"
    await update.message.reply_text(reply, parse_mode='Markdown')

if __name__ == '__main__':
    print("Muz AI OS Server sedang berjalan...")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    app.run_polling()
  
