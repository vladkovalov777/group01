import requests
import json
from pprint import pprint


url = 'https://dummyjson.com/users'
response = requests.get(url)
print(response.content)
print(response.text)
response_json = response.json()
pprint(response_json, indent=4)

with open('users.json', mode='w') as file:
    json.dump(response_json, file, indent=4)