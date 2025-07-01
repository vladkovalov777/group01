from pprint import pprint
import requests

URL = "https://dummyjson.com/users"
params = {
    "limit": 450,
    "skip": 0
}

response = requests.get(url=URL, params=params)
users = response.json()["users"]


young_brown_hair_women = 0

alabama_men_emails = []

for user in users:
    if (
        user["gender"] == "female"
        and user["age"] < 30
        and user["hair"]["color"].lower() == "brown"
    ):
        young_brown_hair_women += 1
    if (
        user["gender"] == "male"
        and user["address"]["state"] == "Alabama"
    ):
        alabama_men_emails.append(user["email"])

print(f"Number of women under 30 with brown hair: {young_brown_hair_women}")
print("Emails of men from Alabama:")
pprint(alabama_men_emails)
