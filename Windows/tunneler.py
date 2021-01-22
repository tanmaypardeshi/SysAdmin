from typing import Optional
from fastapi import FastAPI
from pyngrok import ngrok

app = FastAPI()

url = ngrok.connect(8000).public_url
print(url)


@app.get("/")
def read_root():
    return {"message": "Hi Krisha!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
