import time
import tkinter
class display:
    root = tkinter.Tk()
    root.title("Tic Tac Toe")
    root.geometry("900x900")
    root.resizable(False, False)
    def __init__(self):
        pass

# clear tkinter frame
def clearFrame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    return

# print the board, used for debugging before supporting tkinter
def printBoard(board):
    print("\n")
    for i in range(3):
        for j in range(3):
            if j < 2:
                print(board[i][j], end="| ")
            else:
                print(board[i][j], end=" ")
        print()
    print("\n")
    return

# given a 2d array, return the winner only if each square is filled with x or y
def checkWinner(board):
    # check columns
    for i in range(3):
        if board[0][i] in ['x', 'o']:
            if board[0][i] == board[1][i] and board[1][i] == board[2][i]:
                return board[0][i]
    
    # check rows
    for i in range(3):
        if board[i][0] in ['x', 'o']:
            if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
                return board[i][0]
    
    # check diagonals
    if board[0][0] in ['x', 'o']:
        if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            return board[0][0]
    
    if board[0][2] in ['x', 'o']:
        if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            return board[0][2]
    
    return "none"

# check if the game is over
def checkTie(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                return False
    return True

def calculating():
    # fake calculating
    # note: I added a bit of delay to make it seem like the computer is thinking
    print("calculating...")
    time.sleep(1)
    return

# setup a tic tac toe board as a 2d array
def setupBoard():
    board = []
    for i in range(3):
        board.append([])
        for j in range(3):
            board[i].append(" ")
    return board

# return the final piece location to win given the board and piece
def getWinningMove(board, piece):
    # check columns
    for i in range(3):
        # check if the column is occupied by another piece
        emptySpot = -1
        noMove = False
        for j in range(3):
            if board[i][j] == " ":
                if emptySpot != -1: # if there is an empty spot, break
                    noMove = True
                    break  # 2 empty spaces in the same row, no possible winning move
                emptySpot = j
            elif board[i][j] != piece:
                noMove = True
                break # occupied, no possible winning move
        if not noMove:
            return [i, emptySpot]
        
    # check rows
    for i in range(3):
        # check if the row is occupied by another piece
        emptySpot = -1
        noMove = False
        for j in range(3):
            if board[j][i] == " ":
                if emptySpot != -1:
                    noMove = True
                    break
                emptySpot = j
            elif board[j][i] != piece:
                noMove = True
                break
        
        if not noMove:
            return [emptySpot, i]

    # check diagonals
    emptySpot = -1
    noMove = False
    for i in range(3):
        if board[i][i] == " ":
            if emptySpot != -1:
                noMove = True
                break
            emptySpot = i
        elif board[i][i] != piece:
            noMove = True
            break
    if not noMove:
        return [emptySpot, emptySpot]
    
    emptySpot = -1
    noMove = False
    for i in range(3):
        if board[i][2-i] == " ":
            if emptySpot != -1:
                noMove = True
                break
            emptySpot = i
        elif board[i][2-i] != piece:
            noMove = True
            break
    if not noMove:
        return [emptySpot, 2-emptySpot]
    
    return [-1, -1] # no winning moves in the board

# try adjacents
def tryAdjacents(board, location):
    tries = {
        "up": [location[0]-1, location[1]],
        "down": [location[0]+1, location[1]],
        "left": [location[0], location[1]-1],
        "right": [location[0], location[1]+1],
        "upleft": [location[0]-1, location[1]-1],
        "upright": [location[0]-1, location[1]+1],
        "downleft": [location[0]+1, location[1]-1],
        "downright": [location[0]+1, location[1]+1]
    }
    adjacents = set()

    for key in tries:
        # skip if keys are below 0 or above 2
        if tries[key][0] < 0 or tries[key][0] > 2:
            continue
        if tries[key][1] < 0 or tries[key][1] > 2:
            continue
        # skip if the location is already occupied
        if board[tries[key][0]][tries[key][1]] != " ":
            continue
        adjacents.add(tuple(tries[key]))

    if len(adjacents) == 0:
        return None
    else:
        return adjacents

# find adjacents to a given piece in the board
def findAdjacents(board, piece):
    adjacents = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == piece:
                tempAdjacents = tryAdjacents(board, [i, j])
                if tempAdjacents != None:
                    # combine the adjacents with the existing set
                    adjacents = adjacents.union(tempAdjacents)
    return adjacents