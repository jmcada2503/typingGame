import requests
import time

b = ""
while True:
    try:
        response = requests.get("http://localhost:4000/name")
        if response != b:
            b = response
            if response.status_code == 200:
                data = response.json()
                print("Data:", data)
            else:
                print("Error")
    except:
        print("Refused Connection")
    time.sleep(0.5)
