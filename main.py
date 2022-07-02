import os
import json
import requests
from actions import *
from computer import computer
from local import localGame
from remote import remoteGame
import tkinter


# get server ip from serverIP.txt, this allows the server IP to be changed without changing multiple files
with open("serverIP.txt", "r") as f:
    serverIP = f.read()

def scoreboard():
    # clear frame
    clearFrame(display.root)
    print()

    # request the scores from the server
    onlineScores = json.loads(requests.get(serverIP + "scores").text)

    # get local scores
    scores = json.loads(open("scores.json", "r").read())

    # display local scores on tkinter
    local = tkinter.Label(display.root, text="Local Scores", font=("Arial", 40), anchor="center", width=30)
    local.grid(row=0, column=3, columnspan=6)
    for row, key in enumerate(scores["local"]):
        print(key, ":", scores["local"][key])
        score = tkinter.Label(display.root, text=key + ": " + str(scores["local"][key]), font=("Arial", 20), anchor="center", width=30)
        score.grid(row=row+2, column=3, columnspan=6)

    # print local scores to terminal
    print("Local scores:")
    for key in scores["local"]:
        print(key + ": " + str(scores["local"][key]))

    print()

    rowOffset = len(scores["local"]) + 2

    # display online scores on tkinter
    online = tkinter.Label(display.root, text="Online Scores", font=("Arial", 40), anchor="center", width=30)
    online.grid(row=rowOffset, column=3, columnspan=6)
    for row, key in enumerate(onlineScores):
        print(key, ":", onlineScores[key])
        score = tkinter.Label(display.root, text=key + ": " + str(onlineScores[key]), font=("Arial", 20), anchor="center", width=30)
        score.grid(row=rowOffset+row+2, column=3, columnspan=6)


    # print online scores to terminal
    print("Online scores:")
    
    for key in onlineScores:
        print(key + ": " + str(onlineScores[key]))
    
    # create a button to return to the menu
    menuVar = tkinter.IntVar()
    returnButton = tkinter.Button(display.root, text="Return to menu", font=("Arial", 20), width=30, command=lambda: menuVar.set(1))
    returnButton.grid(row=rowOffset+len(onlineScores)+2, column=3, columnspan=6)
    print()
    print("Return to menu")
    # waits for the return button to be pressed (menuVar is updated when the button is pressed)
    display.root.wait_variable(menuVar)
    display.root.quit() # call main

def menu():
    # clear frame
    clearFrame(display.root)
    # display menu with tkinter
    welcome = tkinter.Label(display.root, text="Welcome to Tic Tac Toe!", font=("Arial", 40), anchor="center", width=30)
    welcome.grid(row=0, column=3, columnspan=6)
    print("Welcome to Tic Tac Toe!")

    print("Please select an option:")
    # computer is a button that calls computer()
    computerButton = tkinter.Button(display.root, text="1. Play against a computer (I'm lonely)", command=computer, font=("Arial", 20), width=30)
    # center the button
    computerButton.grid(row=1, column=3, columnspan=6)
    print("1. Play against a computer (I'm lonely)")

    # local is a button that calls localGame()
    localButton = tkinter.Button(display.root, text="2. Play against a local player", command=localGame().main, font=("Arial", 20), width=30)
    localButton.grid(row=2, column=3, columnspan=6)
    print("2. Play against a local player")

    # remote is a button that calls remoteGame()
    remoteButton = tkinter.Button(display.root, text="3. Play against a remote player", command=remoteGame, font=("Arial", 20), width=30)
    remoteButton.grid(row=3, column=3, columnspan=6)
    print("3. Play against a remote player")

    # scoreboard is a button that calls scoreboard()
    scoreboardButton = tkinter.Button(display.root, text="4. View scoreboard", command=scoreboard, font=("Arial", 20), width=30)
    scoreboardButton.grid(row=4, column=3, columnspan=6)
    print("4. View scoreboard")

    # exit is a button that exits the program
    exitButton = tkinter.Button(display.root, text="5. Exit", command=exit, font=("Arial", 20), width=30)
    exitButton.grid(row=5, column=3, columnspan=6)
    print("5. Exit")

    # display
    display.root.mainloop()

    """print("welcome to tic tac toe! PLease select an option:")
    print("1. Play against a computer (I'm lonely)")
    print("2. Play against a local player")
    print("3. Play against a remote player")
    print("4. Scoreboard")
    print("5. Quit")
    choice = input("Please enter your choice: ")"""

def main():
    # create scores.json if it doesn't exist
    if not os.path.isfile("scores.json"):
        scores = {}
        scores["local"] = {"computer":0,}
        with open("scores.json", "w") as f:
            json.dump(scores, f)

    # call menu
    while True:
        menu()