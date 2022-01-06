import csv
import stdiomask
import time
import colorama
from colorama import Fore, Back, Style

class Login:
    def __init__(self):
        self.data = []
        with open('Database.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    #self.data[row[0]] = row[1]
                    temp = [row[0], row[1], row[2], row[3], row[4], row[5]]
                    self.data.append(temp)
                    line_count += 1
        print(self.data)
        print("Login")
        self.username = input('Username: ')
        self.password = input('Password: ')

    #check info other user

    def check_username_find(self):
        print("Check username:")
        name = input("Enter username: ")
        founded = False
        for i in range(len(self.data)):
            if name in self.data[i][0]:
                founded = True
                print(f"{name} is found: ")
        if founded == False:
            print(f"{name} is not existed")

    # Them ham check online

    def check_username_showfullname(self):
        print("show username's fullname")
        name = input("Enter username: ")
        founded = False
        for i in range(len(self.data)):
            if name in self.data[i][0]:
                founded = True
                print(f"{name}'s fullname: {self.data[i][2]}")
        if founded == False:
            print(f"{name} is not existed")

    def check_username_showdate(self):
        print("show username's date of birth:")
        name = input("Enter username: ")
        founded = False
        for i in range(len(self.data)):
            if name in self.data[i][0]:
                founded = True
                print(f"{name}'s date of birth: {self.data[i][3]}")
        if founded == False:
            print(f"{name} is not existed")

    def check_username_showWinningGame(self):
        print("show username's winning game")
        name = input("Enter username: ")
        founded = False
        for i in range(len(self.data)):
            if name in self.data[i][0]:
                founded = True
                print(f"{name}'s winning game: {self.data[i][4]}")
        if founded == False:
            print(f"{name} is not existed")

    def check_username_showNote(self):
        print("show username's note: ")
        name = input("Enter username: ")
        founded = False
        for i in range(len(self.data)):
            if name in self.data[i][0]:
                founded = True
                print(f"{name}'s Note: {self.data[i][5]}")
        if founded == False:
            print(f"{name} is not existed")

    def check_username_showall(self):
        print("show username's all info")
        name = input("Enter username: ")
        founded = False
        for i in range(len(self.data)):
            if name in self.data[i][0]:
                founded = True
                print(f"{name}'s fullname: {self.data[i][2]}")
                print(f"{name}'s date of birth: {self.data[i][3]}")
                print(f"{name}'s winning game: {self.data[i][4]}")
        if founded == False:
            print(f"{name} is not existed")

    def MenuCheckUser(self):
        print('1) find user.')
        print('2) check if user online.')
        print("3) show user's date of birth.")
        print("4) show user's full name.")
        print("5) show user's winning game")
        print("6) show user's note")
        print("7) show user's all information.")

    #Login

    def login_check(self):
        key1, value1 = self.username, self.password

        #if key1 in self.data and value1 == self.data[key1]:
        ValidAccount = False
        for i in range(len(self.data)):
            if key1 in self.data[i][0] and value1 in self.data[i][1]:
                ValidAccount = True
                print(f'\nWelcome Back {self.username}')
        while ValidAccount == False:
            print("\nWrong Username Or Password")
            ask = input("\nAre You A New User? y/n : ")

            if ask == "y":
                ValidAccount = True
                self.new_user()
            if ask == 'n':
                print("Login")
                check_username = input("\nUsername : ")
                check_password = stdiomask.getpass()

                key, value = check_username, check_password


                #if key in self.data and value == self.data[key]:
                for i in range(len(self.data)):
                    if key in self.data[i][0] and value in self.data[i][1]:
                        ValidAccount = True
                        print(f"\nWELCOME {check_username}!!")

    def new_user(self):
        new_username = input('\nPlease Enter A New Username : ')
        new_password = input('Please Enter A New Password : ')
        new_fullname = input('Please Enter Fullname: ')
        new_dof = input('Please Enter Date Of Birth: ')
        new_note = input('Please Enter your note: ')

        temp = [new_username, new_password, new_fullname, new_dof, 0, new_note]
        self.data.append(temp)

        print("Login: ")
        check_username = input("\nUsername : ")
        check_password = stdiomask.getpass()

        key, value = check_username, check_password

        matched = False
        #if key in self.data and value == self.data[key] :
        for i in range(len(self.data)):
            if key in self.data[i][0] and value in self.data[i][1]:
                matched = True
                print(f"\nWELCOME {check_username}!!")
        if matched == False:
            self.login_check()

    def caesar_encrypt(self):
        word = input('Enter the plain text: ')
        c = ''
        for i in word:
            if (i == ' '):
                c += ' '
            else:
                c += (chr(ord(i) + 3))
        return c

    def caesar_decrypt(self):
        word = input('Enter the cipher text: ')
        c = ''
        for i in word:
            if (i == ' '):
                c += ' '
            else:
                c += (chr(ord(i) - 3))
        return c

    def UpdateDatabase(self):
        with open('Database.csv', mode='w', newline='', encoding='utf-8') as csv_file:
            user_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            user_writer.writerow(["Username", " Password", " Fullname", " Date of birth", " winning game", " Note"])
            user_writer.writerows(self.data)

    def setFullName(self):
        new_FullName = input("Enter your new Full Name: ")
        for i in range(len(self.data)):
            if self.username in self.data[i][0]:
                self.data[i][2] = new_FullName
                print("New fullname: " + str({self.data[i][2]}))

    def setBirthday(self):
        new_DOB = input("Enter your new DOB: ")
        for i in range(len(self.data)):
            if self.username in self.data[i][0]:
                self.data[i][3] = new_DOB
                print("New DOB: " + str({self.data[i][3]}))

    def setNote(self):
        new_Note = input("What are your feelings today? ")
        for i in range(len(self.data)):
            if self.username in self.data[i][0]:
                self.data[i][5] = new_Note
                print("New note: " + str({self.data[i][5]}))

    def showMenu(self):
        print("Please choose the following setting options")
        print("Press 1. Set your full name")
        print("Press 2. Set your birthday")
        print("Press 3. Set your note")
        print("Press other keys: Setting up finished")

def GamePlay():
    boardShipMap = []
    board = []
    #start creating Shipboard
    for x in range(10):
        board.append(["O"] * 10)

    with open('Ship1.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            boardShipMap.append(row)

    #end creating Shipboard

    def print_board(board):
        for row in board:
            print(" ".join(row))

    # starting the game and printing the board

    print ("Let's play Battleship!")
    allShipWereNotSank = False
    while allShipWereNotSank == False:
        print_board(board)

        # asking the user for a guess
        for turn in range(4):
            guess_row = int(input("Guess Row:"))
            guess_col = int(input("Guess Col:"))
            guess_row -= 1
            guess_col -= 1


            # if the user's right, the game ends
            if 0<=guess_row and guess_row <= 9 and boardShipMap[guess_row][guess_col] == "X":
                print ("Congratulations! You hitted a ship")
            else:
                # warning if the guess is out of the board
                if (guess_row < 0 or guess_row > 9) or (guess_col < 0 or guess_col > 9):
                    print("Oops, that's not even in the ocean.")

                # warning if the guess was already made
                elif (board[guess_row][guess_col] == "X"):
                    print("You guessed that one already.")

                # if the guess is wrong, mark the point with an X and start again
                else:
                    print("You missed my battleship!")
                    board[guess_row][guess_col] = "X"

                # Print turn and board again here
                print("Turn " + str(turn + 1) + " out of 4.")
                print_board(board)

        print("")

        print_board(board)

        for i in range(len(boardShipMap)):
            for j in range (len(boardShipMap)):
                if boardShipMap[i][j] != "O":
                    allShipWereNotSank = True
                    print ("Game Over")
                    break
            if allShipWereNotSank == True:
                break
        if allShipWereNotSank == True:
            break

def startPlayingGame():
    while True:
        GamePlay()
        print("Do you want to play again?")
        print("1: Yes")
        print("2: No")
        choice = int(input())
        if choice == 2:
            break

def changeInfoLogin(main):
    main.showMenu()

    while True:
        choice = int(input('Enter one choice (1-3 or other keys): '))
        if choice == 1:
            main.setFullname()
        elif choice == 2:
            main.setBirthday()
        elif choice == 3:
            main.setNote()
        else:
            break

def afterLoginMenu(main):
    while True:
        print('1) Change information')
        print('2) Start game')
        choice = int(input('Enter your choice (1-2): '))
        print()
        if choice == 1:
            changeInfoLogin(main)
        elif choice == 2:
            startPlayingGame()

import csv
def sendingShip2():
    with open('Ship1.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        Board1=[]
        for row in csv_reader:
            Board1.append(row)
        # print()
        # print(Board1)
        listShipBoard1 = []
        for i in range(len(Board1)):
            for j in range(len(Board1[i])):
                if Board1[i][j] == "X":
                    listShipBoard1.append([i,j]) 
        print(listShipBoard1)
        
        print()
        boardString = []
        for row in Board1:
            # row=";".join(row)
            # print(" ".join(row))
            boardString.append(",".join(row))
        # listBorad=";".join(listBorad)
        # print(listBorad)
        boardString= ";".join(boardString)
        # print(boardString)
        
        print()
        board = []
        boardString=boardString.split(";")
        for row in boardString:
            temp = row.split(",")
            board.append(temp)
        
        # print(board)
import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


colorama.init()

board1 = []
board2 = []
def createBoard():
    #start creating Shipboard
    while(len(board1) != 0):
        board1.pop()
    while(len(board2) != 0):
        board2.pop()
    with open('Ship1.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            board1.append(row)
    for x in range(10):
        board2.append(["O"] * 10)

def printTwoBoard():
    # print(Fore.RED)
    # print(Back.CYAN)
    gotoxy(7,3)
    print("Your board")
    
    gotoxy(41,3)
    print("Your opponent's board")
    
    gotoxy(1, 4)
    print(Fore.YELLOW + Back.YELLOW + Style.NORMAL + "HHHHHHHHHHHHHHHHHHHHHHH" + Style.RESET_ALL)
    lineCount = 0
    for row in board1:
        print(Fore.YELLOW + Back.YELLOW + Style.NORMAL + "H " + Style.RESET_ALL + Style.NORMAL, end="")
        # print(Fore.RED + Back.CYAN  + " ".join(row),end="")
        positionCount = 0
        for i in range(len(row)):
            if row[i] == "O":
                print(Fore.WHITE + Back.CYAN  + row[i],end="")
            elif row[i]=="X":
                print(Fore.BLACK + Back.CYAN  + row[i],end="")
            elif row[i]=="D":
                print(Fore.RED + Back.CYAN  + row[i],end="")
            elif row[i]=="M":
                print(Fore.MAGENTA + Back.CYAN  + row[i],end="")
            if positionCount != len(row) - 1:
                print(" ",end = "")
            positionCount += 1
        print(Fore.YELLOW + Back.YELLOW + Style.NORMAL + " H" + Style.RESET_ALL)
    print(Fore.YELLOW + Back.YELLOW + Style.NORMAL + "HHHHHHHHHHHHHHHHHHHHHHH" + Style.RESET_ALL)
    
    print()
    
    x = 40
    y = 4
    gotoxy(x,y)
    y+=1
    print(Fore.YELLOW + Back.YELLOW + Style.NORMAL + "HHHHHHHHHHHHHHHHHHHHHHH" + Style.RESET_ALL)
    lineCount = 0
    for row in board2:
        gotoxy(x,y)
        y += 1
        print(Fore.YELLOW + Back.YELLOW + Style.NORMAL + "H " + Style.RESET_ALL + Style.NORMAL, end="")
        # print(Fore.RED + Back.CYAN  + " ".join(row),end="")
        positionCount = 0
        for i in range(len(row)):
            if row[i] == "O":
                print(Fore.WHITE + Back.CYAN  + row[i],end="")
            elif row[i]=="X":
                print(Fore.BLACK + Back.CYAN  + row[i],end="")
            elif row[i]=="D":
                print(Fore.RED + Back.CYAN  + row[i],end="")
            elif row[i]=="M":
                print(Fore.MAGENTA + Back.CYAN  + row[i],end="")
            if positionCount != len(row) - 1:
                print(" ",end = "")
            positionCount += 1
        print(Fore.YELLOW + Back.YELLOW + Style.NORMAL + " H" + Style.RESET_ALL)
    gotoxy(x,y)
    y+=1
    print(Fore.YELLOW + Back.YELLOW + Style.NORMAL + "HHHHHHHHHHHHHHHHHHHHHHH" + Style.RESET_ALL)

def sendBoardtoServer():
    boardString = []
    for row in board1:
        boardString.append(",".join(row))
    boardString= ";".join(boardString)
    soc.sendall(boardString.encode("utf8"))

def gotoxy(x,y):
    print ("%c[%d;%df" % (0x1B, y, x), end='')

if __name__ == "__main__":
    print("hello1")
    createBoard()
    print("hello2")
    # sendBoardtoServer()
    print("hello3")
    printTwoBoard()