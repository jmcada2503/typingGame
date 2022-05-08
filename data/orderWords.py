import json

words = {"1":[], "2":[], "3":[]}

with open("./spanish.lst", "r") as f:
    data = f.readlines()

for i in range(len(data)):
    data[i] = data[i].replace("\n", "").replace("\\", "ñ") 
    if len(data[i]) <= 5:
        words["1"].append(data[i])
    elif len(data[i]) <= 10:
        words["2"].append(data[i])
    elif len(data[i]) <= 20:
        words["3"].append(data[i])

with open("words.json", "w") as f:
    json.dump(words, f, indent=4, sort_keys=True)
