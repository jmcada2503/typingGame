from getkey import getkey, keys

while True:
    key = getkey()
    try:
        print("Key:", ord(key))
    except Exception as e:
        print("Error:", e)
        print("KeyStr:", key[0])
