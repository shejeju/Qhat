import os
from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = '8160586658:AAGGFpDdsIUar2sYKrt0ZgdOP3rRpfLMRfM'
OPENAI_API_KEY = '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'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"].get("text", "")

        if user_message:
            response_text = get_chatgpt_response(user_message)
            send_message(chat_id, response_text)

    return "ok", 200

def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def get_chatgpt_response(message):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "رد على المستخدم كأنك في محادثة شخصية معه."},
            {"role": "user", "content": message}
        ]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return "حدث خطأ، حاول مرة ثانية."

if __name__ == "__main__":
    app.run()