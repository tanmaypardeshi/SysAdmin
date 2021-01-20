from typing import Optional
from fastapi import FastAPI
from pyngrok import ngrok
import ctypes
import pyperclip

app = FastAPI()

url = ngrok.connect(8000).public_url
pyperclip.copy(url)
user32 = ctypes.windll.user32
user32.MessageBoxW(0, "URI: " + url + " (copied to clipboard)", "DRACO is online", 0)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}