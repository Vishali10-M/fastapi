from fastapi import FastAPI
from app.models import Item
from app.database import database

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    collection = database["items"]
    result = await collection.insert_one(item_dict)
    return {"id": str(result.inserted_id), **item_dict}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    collection = database["items"]
    item = await collection.find_one({"_id": item_id})
    if item is None:
        return {"error": "Item not found"}
    item["id"] = str(item["_id"])
    return item
