import json
import os
import requests
from datetime import date

def load_facts():
    with open("facts.json", encoding="utf-8") as f:
        return json.load(f)

def pick_fact(facts):
    day_of_year = date.today().timetuple().tm_yday
    return facts[day_of_year % len(facts)]

def format_message(fact):
    return (
        f"📌 <b>Факт дня</b>\n"
        f"{fact['fact']}\n\n"
        f"💭 <i>Вопрос для размышления: {fact['question']}</i>\n"
        f"🏷️ Область: {fact['category']}"
    )

def send_telegram(text, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {response.text}")
    response.raise_for_status()

if __name__ == "__main__":
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    facts = load_facts()
    fact = pick_fact(facts)
    message = format_message(fact)
    send_telegram(message, token, chat_id)
