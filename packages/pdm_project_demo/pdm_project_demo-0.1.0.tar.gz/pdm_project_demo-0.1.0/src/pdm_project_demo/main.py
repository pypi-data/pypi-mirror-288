from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index():
    return {"msg": "Hello World!"}


@app.get("/items/{item_id}")
async def get_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
