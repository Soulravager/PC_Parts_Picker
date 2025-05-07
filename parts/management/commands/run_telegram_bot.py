#TO RUN
#>>> 
'''
            python manage.py run_telegram_bot

'''

import time
import requests
from django.core.management.base import BaseCommand
import google.generativeai as genai

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7725781198:AAHaGtm5eh9j-xN1cl1xBFiRKXZ4O72qSUM"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Initialize Gemini API
genai.configure(api_key="AIzaSyBS6zUQANjgspTU1DT4C1PHdfJrmDngOA4")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction=(
        "Only answer computer-related topics. This chat is for a PC builder chatbot.\n"
        "If the user asks something unrelated, either ask for clarification or reply with:\n"
        "'I can only answer that Related to PC Building.'\n"
        "Focus on PC-building or computer hardware/software issues."
    ),
)

# Function to get latest messages from Telegram
def get_updates(offset=None):
    params = {"timeout": 30, "offset": offset}
    response = requests.get(f"{TELEGRAM_API_URL}/getUpdates", params=params)
    return response.json()

# Function to send a message back to the Telegram user
def send_telegram_message(chat_id, text):
    payload = {"chat_id": chat_id, "text": text}
    requests.post(f"{TELEGRAM_API_URL}/sendMessage", json=payload)

# Function to get a response from Gemini AI
def get_gemini_response(prompt):
    try:
        chat_session = model.start_chat(
            history=[{
                "role": "user",
                "parts": [
                    "Only answer computer-related topics. This chat is for a PC builder chatbot.\n"
                    "If the user asks something unrelated, either ask for clarification or reply with:\n"
                    "'I can only answer that in PC Builder.'\n"
                    "Focus on PC-building or computer hardware/software issues.\n"
                    "Make the text short so that it's clear to read.\n"
                    
                ],
            }]
        )
        response = chat_session.send_message(prompt)
        return response.text.strip() if response.text else "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"Error: {e}"

class Command(BaseCommand):
    help = "Runs the Telegram bot that interacts with Gemini AI"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Telegram bot started..."))

        last_update_id = None  # Store last processed update ID

        while True:
            updates = get_updates(last_update_id)

            if updates.get("result"):
                for update in updates["result"]:
                    last_update_id = update["update_id"] + 1  # Prevent duplicate messages

                    if "message" in update:
                        chat_id = update["message"]["chat"]["id"]
                        user_text = update["message"].get("text", "")

                        if user_text:
                            self.stdout.write(self.style.NOTICE(f"Received: {user_text}"))
                            response_text = get_gemini_response(user_text)

                            send_telegram_message(chat_id, response_text)
                            self.stdout.write(self.style.SUCCESS(f"Replied: {response_text}"))

            time.sleep(3)  # Wait before polling again (avoid rate limits)