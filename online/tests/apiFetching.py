import requests

response = requests.get("https://catfact.ninja/fact")

if response.status_code == 200:
    data = response.json()
    print("Data:", data)
    print("Length:", len(data["fact"]))
else:
    print("Error")
