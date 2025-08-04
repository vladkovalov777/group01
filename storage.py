from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import config


class MongoDBStorage:
    def __init__(self):
        uri = f"mongodb+srv://{config.MONGO_USER}:{config.MONGO_PASSWORD}@cluster0.nns1hnu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

        client = MongoClient(uri, server_api=ServerApi("1"))
        self.db = client[config.DATABASE_NAME]
        self.collection = self.db[config.TOUR_COLLECTION]

    def create(self, tour):
        self.collection.insert_one(tour)

    def get_tour(self, pk):
        return self.collection.find_one({"pk": pk})

    def get_tours(self, q="", limit=20, max_price=999999):
        query = {"price": {"$lte": max_price}}
        if q:
            query["title"] = {"$regex": q, "$options": "i"}

        cursor = self.collection.find(query).sort("created_at", -1).limit(limit)
        return list(cursor)

    def update_tour(self, pk, data):
        self.collection.update_one({"pk": pk}, {"$set": data})

    def delete_tour(self, pk):
        self.collection.delete_one({"pk": pk})


storage = MongoDBStorage()
