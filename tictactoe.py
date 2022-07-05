import os, json
# create scores.json if it doesn't exist
if not os.path.isfile("scores.json"):
    scores = {}
    scores["local"] = {"computer":0,}
    with open("scores.json", "w") as f:
        json.dump(scores, f)


from main import *
main()