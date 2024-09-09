import os

from dotenv import load_dotenv
import telebot

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
AUTHORIZED_USERS = [920391928, 7001706700]

BOT = telebot.TeleBot(TELEGRAM_TOKEN)
