import requests
from pprint import pprint


url = 'https://dummyjson.com/users'
response = requests.get(url)
print(response.content)
print(response.text)
response_json = response.json()
pprint(response_json, Lesson20=4)
