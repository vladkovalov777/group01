from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import config


class MongoDBStorage:
    def __init__(self):
        uri = f"mongodb+srv://{config.MONGO_USER}:{config.MONGO_PASSWORD}@cluster0.nns1hnu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

        client = MongoClient(uri, server_api=ServerApi("1"))
        self.db = client[config.DATABASE_NANE]
        self.book_collection = self.db[config.BOOK_COLLECTION]

    def create(self, book_data: dict):
        self.book_collection.insert_one(book_data)

    def get_book(self, pk: str) -> dict:
        query = {"pk": pk}
        result = self.book_collection.find_one(query)
        return result

    def get_books(
        self, q: str = "", limit: int = 10, max_price: float = 5000000
    ) -> list[dict]:

        query = {
            "price": {"$lte": max_price},
            "title": {"$regex": q.strip(), "$options": "i"},
        }
        result = self.book_collection.find(query).limit(limit).sort("price", -1)
        return list(result)

    def delete_book(self, pk: str):
        query = {"pk": pk}
        self.book_collection.delete_one(query)

    def patch_book_image(self, pk: str, image: str):
        query = {"pk": pk}
        updates = {"$set": {"image": image}}
        self.book_collection.update_one(query, updates)

    def update_book(self, pk: str, data: dict):
        query = {"pk": pk}
        updates = {"$set": data}
        self.book_collection.update_one(query, updates)


storage = MongoDBStorage()
