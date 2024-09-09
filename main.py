import os
import uvicorn
from fastapi import FastAPI

from start_boot import start_script

app = FastAPI()

start_script()


@app.get("/")
def read_root():
    return {"message": "Hello, Render!"}


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
