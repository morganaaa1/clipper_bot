import os
from dotenv import load_dotenv
from groq import Groq
from aiogram import Bot, Dispatcher

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()
url_cache = {}  # Database sementara