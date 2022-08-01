# cs11FinalProject
Final project for cs11. Multiplayer tic-tac-toe, with online multiplayer.

# Installation
## Prerequisites
Python v3.6 or higher. \
pip \
git (unless you have a local copy)

## Steps
Note: This has only been tested on Windows 10, results may vary on other operating systems.

1. Clone the repository at https://github.com/TheArchons/cs11FinalProject (or extract the zip file) and move into the directory.
2. Install the dependencies. To do this, run the following command: \
    `pip install -r requirements.txt`

# Usage
Run tictactoe.py in the project directory. To do this, run the following command: \
    `python tictactoe.py` (or `python3 tictactoe.py` if you are on MacOS or Linux

After running the program, a menu will appear. Click on the menu item you want to use.

## Menu items
1. Play against a computer - this allows you to play against a computer. You may then select one of three difficulties:
    1. Easy - the computer will make random moves.
    2. Medium - the computer will make random moves, but will also make a move if it is about to lose.
    3. Hard - Impossible to beat, almost always determines the best move.
2. Play against a local player - this allows you to play against another person on the same computer. You will both be able to select your own names.
3. Play against a remote player - this allows you to play against another person on a different computer. This works by connecting to a server. There is one person that creates a game, and then another person can join the game using the first person's username.
4. View scoreboard - this allows you to view the scoreboard. This is separated into two parts:
    1. Local Scores, which are the scores of players on the same computer, and the computer's score.
    2. Online Scores, which are the scores on the server.
5. Exit - this exits the program.

# Why are there multiple python files?
This is because I wanted to organize the code a bit, as the entire project has more than 2000 lines of code. These are split for their purposes. For example, local.py is the file that contains the code for local games, while test_main.py is for testing with pytest.

# What's the justfile?
The justfile is similar to a shell script, but it is cross-platform and allows multiple commands. More information at **[just](https://github.com/casey/just)**.