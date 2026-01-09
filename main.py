from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import config

uri = f"mongodb+srv://{config.MONGO_USER}:{config.MONGO_PASSWORD}@cluster0.nns1hnu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))
# Send a ping to confirm a successful connection

database = client["books_database"]
books_collection = database["books"]

# READ

print("\n Усі книги:")
for book in books_collection.find():
    print(book)

print("\n Книга з назвою 'Гра престолів':")
book = books_collection.find_one({"назва": "Гра престолів"})
print(book)

print("\n Книги з кількістю сторінок більше 200:")
for book in books_collection.find({"кількість_сторінок": {"$gt": 200}}):
    print(book)

# UPDATE

new_price = 450
result = books_collection.update_one(
    {"назва": "Гра престолів"}, {"$set": {"вартість": new_price}}
)
print(f"\n Оновлено {result.modified_count} книгу(и) — нова ціна: {new_price}")

result = books_collection.update_many({"клас": 9}, {"$set": {"favorite": True}})
print(f"\n Додано поле 'favorite' до {result.modified_count} книги(и)")

#DELETE

delete_result = books_collection.delete_one({"назва": "Основи здоров’я"})
print(f"\n Видалено книгу 'Основи здоров’я' — {delete_result.deleted_count} документ")

delete_many_result = books_collection.delete_many({"кількість_сторінок": {"$lt": 100}})
print(
    f"\n Видалено всі книги з <100 сторінок — {delete_many_result.deleted_count} документ(ів)"
)
