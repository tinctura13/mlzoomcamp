import requests


url = "https//localhost:8060/2015-03-31/functions/function/invocations"

data = {"url": "https://habrastorage.org/webt/rt/d9/dh/rtd9dhsmhwrdezeldzoqgijdg8a.jpeg"}

result = requests.post(url, json=data)


print(result)