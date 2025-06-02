import os
import logging
import requests
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# إعدادات البوت
BOT_TOKEN = "8160586658:AAGGFpDdsIUar2sYKrt0ZgdOP3rRpfLMRfM"
OPENAI_API_KEY = "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"

# تهيئة البوت
bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)

# رد على كل رسالة (نص أو صورة)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        await update.message.reply_text("📸 استقبلت صورة، بس الرد على الصور مش مفعل حالياً.")
    elif update.message.text:
        await update.message.reply_text(f"🧠 رد تلقائي على: {update.message.text}")

# نقطة البداية للويب هوك
@app.route('/')
def home():
    return '✅ البوت شغال على Render'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        application.add_handler(MessageHandler(filters.ALL, handle_message))
        application.process_update(update)
        return "ok"
    return "not ok"

# تشغيل السيرفر على Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)