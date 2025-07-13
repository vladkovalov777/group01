from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import config

uri = f"mongodb+srv://{config.MONGO_USER}:{config.MONGO_PASSWORD}@cluster0.nns1hnu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))
# Send a ping to confirm a successful connection

database = client["books_database"]
books_collection = database["books"]

got_book = {
    "назва": "Гра престолів",
    "вартість": 350,
    "рік_випуску": 1996,
    "кількість_сторінок": 694,
}
books_collection.insert_one(got_book)

school_books = [
    {"назва": "Математика 9 клас", "клас": 9, "кількість_сторінок": 230},
    {"назва": "Фізика для школярів", "клас": 9, "кількість_сторінок": 210},
    {"назва": "Історія України. Частина 1", "клас": 9, "кількість_сторінок": 255},
    {"назва": "Англійська мова. Рівень B1", "клас": 9, "кількість_сторінок": 185},
    {"назва": "Основи здоров’я", "клас": 9, "кількість_сторінок": 170},
]
books_collection.insert_many(school_books)


try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
