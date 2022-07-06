import requests
import json
from actions import *
# import asyncio

# get server ip from serverIP.txt
with open("serverIP.txt", "r") as f:
    serverIP = f.read()

class remoteGame():
    playerList = json.loads(requests.get(serverIP + "players").text)
    AmHost = False
    hostName = ""
    username = ""
    opponentName = ""
    opponentPiece = ""
    yourPiece = ""
    game = None
    continueVar = tkinter.IntVar()
    display = display()
    forbiddenNames = [""]
    opponentAction = tkinter.IntVar()

    def main(self):
        # clear frame
        clearFrame(display.root)

        # get player name
        self.getPlayerName()

        # join or start
        self.joinOrStart()

        if self.AmHost == True:
            # host game
            shouldQuit = self.hostGame()
            if shouldQuit == -1:
                display.root.quit()
                return
        else:
            # join game
            self.joinGame()
        
        # game
        self.game()

        # update scores
        self.updateScores()

        # wait for continue button
        display.root.wait_variable(self.continueVar)

        # return to menu
        display.root.quit()

        return
    
    # async function to get opponent
    async def getOpponent(self):
        while True:
            # get current game
            players = requests.get(serverIP + "games/" + self.username)

            # if the opponent has joined, break
            # if response is 200, then the opponent has joined
            if players.status_code == 200:
                # update opponent name
                players = json.loads(players.text)
                self.opponentName = players["opponent"]

                # update your piece
                self.yourPiece = players["hostPiece"]

                # update opponent piece
                if self.yourPiece == "x":
                    self.opponentPiece = "o"
                else:
                    self.opponentPiece = "x"
                
                # update self.opponentAction
                self.opponentAction.set(2)

    # waiting for opponent
    def waitingForOpponent(self):
        # create popup
        popup = tkinter.Toplevel(display.root)
        popup.title("Waiting for Opponent")
        popup.geometry("300x300")
        popup.resizable(False, False)

        # add text to popup
        text = tkinter.StringVar()
        text.set("Waiting for opponent to join...")
        textLabel = tkinter.Label(popup, textvariable=text)

        # add a return to menu button
        returnButton = tkinter.Button(popup, text="Return to Menu", command=lambda: self.opponentAction.set(1))

        # add text and button to popup
        textLabel.pack()
        returnButton.pack()
        
        # call getOpponent function
        self.getOpponent()

        # wait for opponent to join
        display.root.wait_variable(self.opponentAction)

        # destroy popup
        popup.destroy()

        # if opponentAction is 1, return to menu (return button pressed)
        if self.opponentAction.get() == 1:
            return -1
        # if opponentAction is 2, opponent has joined
        else:
            return

    # host game
    def hostGame(self):
        self.hostName = self.username

        # send a request to the server to host a game
        PostRequest = requests.post(serverIP + "startGame", data={"playerName": self.username})
        if PostRequest.status_code == 400:
            self.otherHost()
            return -1
        
        # waiting for opponent
        return self.waitingForOpponent()
        

        """            
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
            print()"""

    # popup to ask if user wants to host or join a game
    def joinOrStart(self):
        # create popup
        popup = tkinter.Toplevel(display.root)
        popup.title("Join or Start a Game")
        popup.geometry("300x300")
        popup.resizable(False, False)

        # text to ask if user wants to host or join a game
        text = tkinter.StringVar()
        text.set("Join or Start a Game?")
        textLabel = tkinter.Label(popup, textvariable=text)
        textLabel.pack()

        # wait for update variable
        joinOrStartVar = tkinter.IntVar()
        joinButton = tkinter.Button(popup, text="Join", command=lambda: joinOrStartVar.set(0))
        joinButton.pack()
        startButton = tkinter.Button(popup, text="Start", command=lambda: joinOrStartVar.set(1))
        startButton.pack()

        # wait for user to click either button
        popup.wait_variable(joinOrStartVar)
        popup.destroy()

        # update AmHost variable
        if joinOrStartVar.get() == 0:
            self.AmHost = False
        else:
            self.AmHost = True

    # forbidden name popup
    def forbiddenPopup(self):
        # create popup
        popup = tkinter.Toplevel(display.root)
        popup.title("ERROR: Forbidden Name")
        popup.geometry("300x300")
        popup.resizable(False, False)
        
        # text saying name is taken or forbidden
        text = tkinter.StringVar()
        text.set("ERROR: Name is taken or forbidden. \n Please try a different name.")
        textLabel = tkinter.Label(popup, textvariable=text)
        textLabel.pack()

        # continue button
        continueButton = tkinter.Button(popup, text="Continue", command=lambda: popup.destroy())
        continueButton.pack()

        # wait for user to click continue button
        popup.wait_window(continueButton)

        return

    # yes/no popup to use existing score
    def useExistingScorePopup(self):
        # create popup
        popup = tkinter.Toplevel(display.root)
        popup.title("Use Existing Score")
        popup.geometry("300x300")
        popup.resizable(False, False)

        # text to ask if user wants to use existing score
        text = tkinter.StringVar()
        text.set("Name already taken, use existing score?")
        textLabel = tkinter.Label(popup, textvariable=text)
        textLabel.pack()

        # yes button and no button
        yesNoVar = tkinter.IntVar() # 0 for yes, 1 for no
        yesButton = tkinter.Button(popup, text="Yes", command=lambda: yesNoVar.set(0))
        yesButton.pack()
        noButton = tkinter.Button(popup, text="No", command=lambda: yesNoVar.set(1))
        noButton.pack()

        # wait for user to click either button
        popup.wait_variable(yesNoVar)
        popup.destroy()

        # close popup when either button is clicked
        if yesNoVar.get() == 0:
            return True
        else:
            return False

    def namePopup(self):
        # tkinter popup to get player name
        popup = tkinter.Toplevel(display.root)
        popup.title("Enter your name")
        popup.geometry("600x300")
        popup.resizable(False, False)

        # create a label and entry for the player name
        nameLabel = tkinter.Label(popup, text="Enter your name:", font=("Arial", 20), anchor="center", width=30)
        nameLabel.grid(row=0, column=0, columnspan=2)
        nameEntry = tkinter.Entry(popup, font=("Arial", 20), width=30)
        nameEntry.grid(row=1, column=0, columnspan=2)

        # submit button
        submitVar = tkinter.IntVar()
        submitButton = tkinter.Button(popup, text="Submit", font=("Arial", 20), width=30, command=lambda: submitVar.set(1))
        submitButton.grid(row=2, column=0, columnspan=2)

        # wait for submit button to be pressed
        display.root.wait_variable(submitVar)

        self.username = nameEntry.get()

        # close popup when submit button is pressed
        popup.destroy()
        return self.username

    def getPlayerName(self):
        while True:
            # get player's name
            username = self.namePopup()

            # check if the name is forbidden
            if username in self.forbiddenNames:
                self.forbiddenPopup()
                continue
            elif username in self.playerList:
                useExisting = self.useExistingScorePopup() # popup if name in scores
                if useExisting:
                    break
            else: # name is not in scores, quit
                break


# online game
"""def remoteGame():
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

    return"""