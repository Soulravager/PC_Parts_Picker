import time
import requests
from django.core.management.base import BaseCommand
import google.generativeai as genai

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7725781198:AAHaGtm5eh9j-xN1cl1xBFiRKXZ4O72qSUM"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Initialize Gemini API with image support
genai.configure(api_key="AIzaSyBS6zUQANjgspTU1DT4C1PHdfJrmDngOA4")
model = genai.GenerativeModel("gemini-1.5-pro")  # Supports images

# Function to get latest messages from Telegram
def get_updates(offset=None):
    params = {"timeout": 30, "offset": offset}
    response = requests.get(f"{TELEGRAM_API_URL}/getUpdates", params=params)
    return response.json()

# Function to send a text message to the Telegram user
def send_telegram_message(chat_id, text):
    payload = {"chat_id": chat_id, "text": text}
    requests.post(f"{TELEGRAM_API_URL}/sendMessage", json=payload)

# Function to download an image from Telegram
def download_telegram_photo(file_id):
    file_info = requests.get(f"{TELEGRAM_API_URL}/getFile?file_id={file_id}").json()
    if "result" in file_info:
        file_path = file_info["result"]["file_path"]
        image_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
        return requests.get(image_url).content  # Returns raw image data
    return None

# Function to get a response from Gemini AI (text & images)
def get_gemini_response(prompt, image_data=None):
    try:
        if image_data:
            response = model.generate_content([prompt, image_data])  # Send both text and image
        else:
            response = model.generate_content(prompt)

        return response.text.strip() if response.text else "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"Error: {e}"

class Command(BaseCommand):
    help = "Runs the Telegram bot that interacts with Gemini AI and supports images"

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

                        # Check if the message contains a photo
                        if "photo" in update["message"]:
                            file_id = update["message"]["photo"][-1]["file_id"]  # Get highest resolution
                            image_data = download_telegram_photo(file_id)

                            if image_data:
                                self.stdout.write(self.style.NOTICE("Received an image. Processing..."))
                                response_text = get_gemini_response("Describe this image:", image_data)
                                send_telegram_message(chat_id, response_text)
                                self.stdout.write(self.style.SUCCESS(f"Replied: {response_text}"))
                            else:
                                send_telegram_message(chat_id, "Sorry, I couldn't download the image.")

                        elif user_text:  # If it's a text message
                            self.stdout.write(self.style.NOTICE(f"Received: {user_text}"))
                            response_text = get_gemini_response(user_text)
                            send_telegram_message(chat_id, response_text)
                            self.stdout.write(self.style.SUCCESS(f"Replied: {response_text}"))

            time.sleep(3)  # Wait before polling again (avoid rate limits)
