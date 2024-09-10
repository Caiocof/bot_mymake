import os
import threading
import uvicorn
from fastapi import FastAPI
import telebot

from start_boot import start_script

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}


def start_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))


if __name__ == "__main__":
    # Inicia o FastAPI e o bot do Telegram em threads separadas
    fastapi_thread = threading.Thread(target=start_fastapi)
    bot_thread = threading.Thread(target=start_script)

    fastapi_thread.start()
    bot_thread.start()

    fastapi_thread.join()
    bot_thread.join()
