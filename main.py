import os
import json
import requests
from actions import *
from computer import computer
from local import localGame
from remote import remoteGame

# get server ip from serverIP.txt, this allows the server IP to be changed without changing multiple files
with open("serverIP.txt", "r") as f:
    serverIP = f.read()

def scoreboard():
    print()
    # request the scores from the server
    onlineScores = json.loads(requests.get(serverIP + "scores").text)
    # get local scores
    scores = json.loads(open("scores.json", "r").read())
    print("Local scores:")
    for key in scores["local"]:
        print(key + ": " + str(scores["local"][key]))

    print()

    print("Online scores:")
    
    for key in onlineScores:
        print(key + ": " + str(onlineScores[key]))
    
    input("press enter to continue...")
    print()

def menu():
    print("welcome to tic tac toe! PLease select an option:")
    print("1. Play against a computer (I'm lonely)")
    print("2. Play against a local player")
    print("3. Play against a remote player")
    print("4. Scoreboard")
    print("5. Quit")
    choice = input("Please enter your choice: ")
    return choice

def main():
    # create scores.json if it doesn't exist
    if not os.path.isfile("scores.json"):
        scores = {}
        scores["local"] = {"computer":0,}
        with open("scores.json", "w") as f:
            json.dump(scores, f)

    choice = menu()
    while choice != "5":
        if choice == "1":
            computer()
        elif choice == "2":
            localGame()
        elif choice == "3":
            remoteGame()
        elif choice == "4":
            scoreboard()
        else:
            print("Invalid choice", end="\n\n")
        choice = menu()