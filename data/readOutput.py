import os
import time

while True:
    data = os.popen("cat ./out.txt")
    print(data.read())
    time.sleep(0.05)
