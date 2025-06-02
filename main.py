import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = "8160586658:AAGGFpDdsIUar2sYKrt0ZgdOP3rRpfLMRfM"

logging.basicConfig(level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        await update.message.reply_text("تم استلام الصورة ✅")
    elif update.message.text:
        await update.message.reply_text(f"رد تلقائي: {update.message.text}")
    else:
        await update.message.reply_text("تم استلام محتوى")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))

app.run_polling()