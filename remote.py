import requests
import json
from actions import *

# get server ip from serverIP.txt
with open("serverIP.txt", "r") as f:
    serverIP = f.read()

# online game
def remoteGame():
    print()
    # get list of players
    players = requests.get(serverIP + "players").text
    # convert from json to list
    players = json.loads(players)

    # get player name
    while True:
        playerName = input("Enter your name: ")
        if playerName not in players:
            break
        else:
            useAnyways = input("Name already taken, use anyways? (y/n) ")
            if useAnyways == "y":
                break
            else:
                continue

    joinOrStart = ""
    hostName = ""
    amHost = False
    
    while joinOrStart not in ["1", "2", "3"]:
        # ask if they would like to join or start a game
        print("Would you like to join or start a game?")
        print("1. Join")
        print("2. Start")
        print("3. Back")
        print()
        joinOrStart = input("Choice: ")
        if joinOrStart == "1":
            while True:
                opponentName = input("please enter the opponent's username: ")
                # send a request to join the game
                join = requests.post(serverIP + "join/" + opponentName, data={"name": playerName})
                # if the request was successful, get the host's name
                if join.status_code == 200:
                    players = json.loads(requests.get(serverIP + "games/" + opponentName).text)
                    hostName = opponentName
                    break
                elif join.status_code == 400:
                    print("No available game found.")
                    continue
                elif join.status_code == 401:
                    print("Your username is the same as the opponent's.")
                    continue
        elif joinOrStart == "2":
            hostName = playerName
            amHost = True
            # send a request to the server to start a game
            PostRequest = requests.post(serverIP + "startGame", data={"playerName": playerName})
            if PostRequest.status_code == 400:
                print("Someone else is already hosting a game with this username.")
                joinOrStart = "-1"
                continue
            print("Waiting for opponent...")
            # wait for the opponent to join
            seconds = 0
            while True:
                time.sleep(1)
                seconds += 1
                if seconds == 30: # ask if they want to return to the menu every 30 seconds
                    continueSearching = input("Continue searching for opponent? (y/n) ")
                    if continueSearching == "y":
                        seconds = 0
                        continue
                    else:
                        print("Exiting...")
                        return
                players = requests.get(serverIP + "games/" + playerName)
                # if the opponent has joined, break
                # if response is 200, then the opponent has joined
                if players.status_code == 200:
                    # convert from json to dictionary
                    players = json.loads(players.text)
                    break
            # opponent has joined, get their name
            opponentName = players["opponent"]
            # start the game
            print("Opponent found!")
            print("Starting game...")
            print()
        elif joinOrStart == "3":
            return
        else:
            print("Invalid choice")

        # set the pieces
        piece = players["hostPiece"]
        if not amHost:
            if piece == "x":
                piece = "o"
            else:
                piece = "x"
            
        # after the game has started
        gameOver = False
        while True:
            # while it is not the player's turn, wait
            print("Waiting for opponent...")
            while True:
                # get the board
                board = requests.get(serverIP + "games/" + hostName)
                # convert from json to dictionary
                board = json.loads(board.text)
                # if the game is over, break and set gameOver to true
                if board["isOver"] == True:
                    gameOver = True
                    break
                # if it is the player's turn, break
                if board["isXTurn"] == True:
                    if piece == "x":
                        break
                else:
                    if piece == "o":
                        break
                # wait for the opponent to make a move
                time.sleep(1)
            # if the game is over, break
            if gameOver == True:
                break
            print("It's your turn!")
            printBoard(board["board"])
            # get them to select the column and row, and it must be empty
            while True:
                row = input("Select a row: ")
                column = input("Select a column: ")
                if column in ["0", "1", "2"] and row in ["0", "1", "2"] and board["board"][int(row)][int(column)] == " ":
                    break
                else:
                    print("Invalid selection")
            
            # update board
            board["board"][int(row)][int(column)] = piece

            # print the updated board
            printBoard(board["board"])

            # send the move to the server
            requests.post(serverIP + "move/" + hostName, data={"column": column, "row": row})
    
    if gameOver == True:
        print("Game over!")
        if board["winner"] == playerName:
            print("You won!")
        else:
            print("You lost!")
        printBoard(board["board"])
        # send the confirmDelete request to the server
        requests.post(serverIP + "confirmDelete/" + hostName)

    return