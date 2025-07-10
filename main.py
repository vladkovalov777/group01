from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import config

uri = f"mongodb+srv://{config.MONGO_USER}:{config.MONGO_PASSWORD}@cluster0.nns1hnu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))
# Send a ping to confirm a successful connection

database = client["warehouse"]
books_collection = database["books"]
mops_collection = database["mops"]

# CREATE
## single

book1 = {"title": "10 negro", "price": 325}
books_collection.insert_one(book1)

## many
mops = [{"price": 125, "series": "FFFD"}]
mops_collection.insert_many(mops)
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
