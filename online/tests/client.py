import requests

response = requests.get("http://localhost:4000/")

if response.status_code == 200:
    data = response.json()
    print("Data:", data)
else:
    print("Error")
