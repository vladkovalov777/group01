import requests

URL = "https://dummyjson.com/carts"
params = {
    "limit": 100,
    "skip": 0
}
response = requests.get(URL, params=params)
orders = response.json()["carts"]

total_cost = 0

for order in orders:
    if order["userId"] <= 25:
        total_cost += order["total"]

print(f"Общая стоимость заказов пользователей с ID <= 25: {total_cost}")