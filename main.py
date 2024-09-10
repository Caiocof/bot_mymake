from fastapi import FastAPI, Request
import telebot

from bot_config import BOT

app = FastAPI()


@app.post("/webhook")
async def telegram_webhook(request: Request):
    json_str = await request.json()
    update = telebot.types.Update.de_json(json_str)
    BOT.process_new_updates([update])
    return {"status": "ok"}


@app.on_event("startup")
async def on_startup():
    webhook_url = f"https://https://telegram-chat-tn5z.onrender.com/webhook"
    BOT.remove_webhook()
    BOT.set_webhook(url=webhook_url)


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI and Telegram bot webhook!"}
