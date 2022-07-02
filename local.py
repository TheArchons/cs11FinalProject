import json
from actions import *

class localGame():
    scores = json.loads(open("scores.json", "r").read())
    board = setupBoard()
    players = ()
    display = display()
    forbiddenNames = [""]

    def main(self):
        # clear frame
        clearFrame(display.root)

        # select user names and update into players
        self.selectUserNames()

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

    # popup to select user. If the name is taken, ask the user if they want to use the existing score with tkinter
    def selectUserPopup(self,player):
        # create popup
        popup = tkinter.Toplevel(display.root)
        popup.title("Select User")
        popup.geometry("300x300")
        popup.resizable(False, False)

        # text to ask if user wants to use existing score
        text = tkinter.StringVar()
        text.set("Enter name for " + player + ":")
        textLabel = tkinter.Label(popup, textvariable=text)
        textLabel.pack()

        # entry box to enter name
        name = tkinter.StringVar()
        nameEntry = tkinter.Entry(popup, textvariable=name)
        nameEntry.pack()

        # submit button with wait
        submitVar = tkinter.IntVar()
        submitButton = tkinter.Button(popup, text="Submit", command=lambda: submitVar.set(1))
        submitButton.pack()
        
        submitButton.wait_variable(submitVar)

        # close popup when submit button is clicked
        popup.destroy()
        return name.get()
    
    def selectUser(self, user):
        while True:
            username = self.selectUserPopup(user)
            if username in self.forbiddenNames:
                self.forbiddenPopup() # popup if name is taken
                continue
            if username in self.scores["local"]:
                useExisting = self.useExistingScorePopup() # popup if name in scores
                if useExisting:
                    break
            else:
                # add name to scores if it does not exist
                self.scores["local"][username] = 0
                break

        # add name to forbidden names
        self.forbiddenNames.append(username)
        
        return username

    # select usernames for the two players. If the name is taken, ask the user if they want to use the existing score with tkinter
    def selectUserNames(self):
        # popup to select players
        print("Select players for x and y")
        self.players = (self.selectUser("X"), self.selectUser("O"))
        print("Players: " + str(self.players))
        return


# a local 1v1 game
"""def localGame():
    print()
    scores = json.loads(open("scores.json", "r").read())

    print("Welcome! Please enter your names: ")
    while True:
        playerX = input("X: ")
        if playerX in scores["local"]:
            useScore = input("name already taken, use existing score? (y/n) ")
            if useScore == "y":
                break
            else:
                continue
        else:
            scores["local"][playerX] = 0
            break
    while True:
        playerO = input("O: ")
        if playerO == playerX:
            print("names must be different")
            continue
        if playerO in scores["local"]:
            useScore = input("name already taken, use existing score? (y/n) ")
            if useScore == "y":
                break
            else:
                continue
        else:
            scores["local"][playerO] = 0
            break

    board = setupBoard()
    isXTurn = True
    while checkWinner(board) == "none" and not checkTie(board):
        if isXTurn:
            print()
            print("X's turn")
            printBoard(board)
            while True:
                x = int(input("Please enter a row: "))
                y = int(input("Please enter a column: "))
                if board[x][y] == " ":
                    break
                print("That square is already taken")
            board[x][y] = "x"
            isXTurn = False
        else:
            print()
            print("O's turn")
            printBoard(board)
            while True:
                x = int(input("Please enter a row: "))
                y = int(input("Please enter a column: "))
                if board[x][y] == " ":
                    break
                print("That square is already taken")
            board[x][y] = "o"
            isXTurn = True
    printBoard(board)

    # add scores
    if checkWinner(board) == "x":
        print("{} wins!".format(playerX))
        scores["local"][playerX] += 1
    elif checkWinner(board) == "o":
        print("{} wins!".format(playerO))
        scores["local"][playerO] += 1
    else:
        print("Tie!")
    print()

    # print scores
    print("Current scores:")
    print(playerX + ": " + str(scores["local"][playerX]))
    print(playerO + ": " + str(scores["local"][playerO]))

    # save scores
    open("scores.json", "w").write(json.dumps(scores))

    # press enter to continue
    input("Press enter to continue...")
    print()

    return # return to menu"""