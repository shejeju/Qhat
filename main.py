import os
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, filters, CallbackContext
import openai

TOKEN = "8160586658:AAGGFpDdsIUar2sYKrt0ZgdOP3rRpfLMRfM"
OPENAI_API_KEY = "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"

app = Flask(__name__)
bot = Bot(token=TOKEN)
openai.api_key = OPENAI_API_KEY

dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.effective_chat.id
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}]
    )
    reply = response.choices[0].message.content
    bot.send_message(chat_id=chat_id, text=reply)

dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Bot is running."

if __name__ == "__main__":
    bot.set_webhook(f"https://YOUR_RENDER_URL.onrender.com/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))