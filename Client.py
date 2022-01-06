import socket
import csv
from random import randint
import socket
from time import sleep, time
import tqdm
import os
import threading
import stdiomask
import time
import colorama
from colorama import Fore, Back, Style

colorama.init()

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step
usernameLoginSuccessful = []
recieveInvitation = False

#------------Cac ham thuong xuyen dung------------

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def waiting2sAndCleanConsole():
    print("Loading...")
    time.sleep(2)
    clearConsole()

#------------End Cac ham thuong xuyen dung------------


#begin client-sever section

def chooseSever():
    global SERVER_ADDRESS
    SERVER_ADDRESS = input("Pls choose Sever address: ")
    global PORT
    PORT =  12121 #int(input("Pls choose a port: "))

def createClient():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    try:
        soc.connect((SERVER_ADDRESS, PORT))
        loginSuccessful = False
        username = ''
        while loginSuccessful == False:
            if Login(soc) == True:
                loginSuccessful = True
            else:
                print("\nWrong Username Or Password")
                print("\nAre You A New User? y/n : ")
                choice = input('Enter your choice (y-n): ')
                if choice == 'y':
                    soc.sendall("create new user".encode("utf8"))
                    createNewUser(soc)
                else:
                    soc.sendall("do not create new user".encode("utf8"))
            waiting2sAndCleanConsole()

        # After Login successful:

        choice = 0
        while choice != 4:
            choice = MenuAftarLogin()
            if choice == 1:
                soc.sendall("change password".encode("utf8"))
                ChangePassword(soc)
            elif choice == 2:
                soc.sendall("check user info".encode("utf8"))
                CheckUserinfo(soc)
            elif choice == 3:
                soc.sendall("setup info".encode("utf8"))
                SetupInfo(soc)
            elif choice == 4:
                soc.sendall("play game".encode("utf8"))
            if choice !=4:
                waiting2sAndCleanConsole()
            else:
                clearConsole()
        # ----------create room----
        startingRoomAndRecieveInvitation(soc)
        # ----------end create room----

        # -------------game play---------
        GamePlay(soc)
        
        #draft
        # content1 = soc.recv(1024).decode("utf8") #recieve
        # soc.sendall(content2.encode("utf8")) #send
        #end draft

    except:
        print("Server hasn't been install: ")
    finally:
        soc.close()

#----------Waiting Room------

messageWhenJoinRoomList = ""

def startingRoomAndRecieveInvitation(soc):
    startGameCommand = input("Enter start game command: ")
    while startGameCommand != "start_game":
        print("Wrong command, please enter again")
        startGameCommand = input("Enter start game command: ")
    soc.sendall(startGameCommand.encode("utf8"))
    opponentAcceptCreateRoom = False
    while opponentAcceptCreateRoom == False:
        listOnlineUser = soc.recv(1024).decode("utf8").split(';')
        for i in range(len(listOnlineUser)):
            print(f"User {i + 1}: {listOnlineUser[i]}")
        foundUserName = False
        while foundUserName == False:
            roomID = input("create_room (choose ID room): ")
            soc.sendall("creatingIDRoom".encode("utf8"))
            messageWhenJoinRoomList = soc.recv(1024).decode("utf8").split(";")
            print(f"messageWhenJoinRoomList: {messageWhenJoinRoomList}")
            if messageWhenJoinRoomList[0]=="SomeOneInviteYouToARoom":
                print("you have an Invitation...")
                time.sleep(2)
                if recieveInviteCreateRoom(soc, messageWhenJoinRoomList) == True:
                    GamePlay(soc)
                    return
            else:
                time.sleep(2)
                soc.sendall("NoInvitation".encode("utf8"))
                
            username2 = input("with (enter username): ")
            soc.sendall("choosingUserName".encode("utf8"))
            messageWhenJoinRoomList = soc.recv(1024).decode("utf8")
            if len(messageWhenJoinRoomList.split(';'))>1:
                print("you have a Invitation...")
                time.sleep(2)
                if recieveInviteCreateRoom(soc) == True:
                    GamePlay(soc)
                    return
            else:
                time.sleep(2)
                soc.sendall("NoInvitation".encode("utf8"))
                
            for i in range(len(listOnlineUser)):
                if username2 == listOnlineUser[i]:
                    foundUserName = True
                    break
            if foundUserName == False:
                print("username is unavailable, please create create room again!")
            while len(messageWhenJoinRoomList) != 0:
                messageWhenJoinRoomList = ""
        listRoominfo = [roomID, usernameLoginSuccessful[0], username2]
        print(f'listRoominfo: {listRoominfo}')
        #someoneInviteToRoomSignal = soc.recv(1024).decode("utf8")
        #if someoneInviteToRoomSignal == 'SomeOneInviteYouToARoom':
        soc.sendall(';'.join(listRoominfo).encode("utf8"))
        print("Waiting for accept invitation...")
        acceptRoomSignal = soc.recv(1024).decode("utf8")
        print(f'acceptRoomSignal: {acceptRoomSignal}')
        if acceptRoomSignal == "Accepted_create_room":
            print("invitation is accepted")
            opponentAcceptCreateRoom = True
            GamePlay(soc)
        else:
            print("invitation is rejected")

            
def recieveInviteCreateRoom(soc, message):
    print("hello1")
    removeJustDoItSignal = soc.recv(1024).decode("utf8")
    print("hello2")
    
    print(f'removeJustDoItSignal: {removeJustDoItSignal}')
    print(f"{message[2]} invite you to room {message[1]}")
    choice = input("Enter your choice (y/n): ")
    if choice == 'y':
        soc.sendall("Accept".encode("utf8"))
        time.sleep(0.5)
        soc.sendall("hasAInvitation".encode("utf8"))
        return True
    else:
        soc.sendall("Reject".encode("utf8"))
        clearConsole()
        return False
#----------End Waiting Room------


#end phan dang lam

#end client-sever section

#begin Login section

def Login(soc):
    def caesar_encrypt(word):
        c = ''
        for i in word:
            if (i == ' '):
                c += ' '
            else:
                c += (chr(ord(i) + 3))
        return c
    def printWaiting():
        for i in range(11):
            percent = i*10
            print(f"Loading: {percent}%")
            time.sleep(0.3)
    username = input('Username: ')
    password = stdiomask.getpass("Password: ")
    originalUserName = username
    print('Do you wanna encrypt account before sending?')
    print('1) Yes')
    print('2) No')
    choice = int(input('Enter your choice (1-2): '))
    if choice == 1:
        username = caesar_encrypt(username)
        password = caesar_encrypt(password)
        soc.sendall("Encrypted".encode("utf8"))
    elif choice == 2:
        soc.sendall("No Encrypted".encode("utf8"))
    loginInfo = [username, password]
    soc.send(';'.join(loginInfo).encode("utf8"))
    loginSuccessfulSignal = soc.recv(1024).decode("utf8")
    printWaiting()
    clearConsole()
    if loginSuccessfulSignal == "Login Successful":
        usernameLoginSuccessful.append(originalUserName)
        print('Login successful!!!!')
        print(f'\nWelcome Back {originalUserName}')
        return True
    else:
        return False

def createNewUser(soc):
    new_username = input('\nPlease Enter A New Username : ')
    new_password = input('Please Enter A New Password : ')
    new_fullname = input('Please Enter Fullname: ')
    new_dof = input('Please Enter Date Of Birth: ')
    new_note = input('Please Enter your note: ')
    newUserObjectList = [new_username, new_password, new_fullname, new_dof, "0", new_note, "offline"]
    soc.sendall(';'.join(newUserObjectList).encode("utf8"))
    print('Ending create new user')

#end Login section

#begin after login section

def MenuAftarLogin():
    print('1) Change password')
    print('2) Check user')
    print('3) Setup info')
    print('4) Start game')
    choice = int(input('Enter your choice (1-4): '))
    return choice

def CheckUserinfo(soc):

    def check_username_find(soc):
        print("Check user exist:")
        name = input("Enter username: ")
        soc.sendall(name.encode("utf8"))
        checkFound = soc.recv(1024).decode("utf8")
        if checkFound == "Found":
            print('Account existed!')
        else:
            print('Account does not existed')

    def check_username_online(soc):
        print("Check user online:")
        name = input("Enter username: ")
        soc.sendall(name.encode("utf8"))
        checkFound = soc.recv(1024).decode("utf8")
        if checkFound == "Found":
            onlineUserStatus = soc.recv(1024).decode("utf8")
            if onlineUserStatus == 'online':
                print("User is online")
            else:
                print("User is offline")
        else:
            print('Account does not existed')

    def check_username_showfullname(soc):
        print("show username's fullname")
        name = input("Enter username: ")
        soc.sendall(name.encode("utf8"))
        founded = False
        checkFound = soc.recv(1024).decode("utf8")
        if checkFound == "Found":
            fullname = soc.recv(1024).decode("utf8")
            print(f"{name}'s fullname: {fullname}")
        else:
            print(f"{name} is not existed")

    def check_username_showdate(soc):
        print("show username's date of birth:")
        name = input("Enter username: ")
        founded = False
        soc.sendall(name.encode("utf8"))
        checkFound = soc.recv(1024).decode("utf8")
        if checkFound == "Found":
            dof = soc.recv(1024).decode("utf8")
            print(f"{name}'s date of birth: {dof}")
        else:
            print(f"{name} is not existed")

    def check_username_showWinningGame(soc):
        print("show username's show winning game:")
        name = input("Enter username: ")
        founded = False
        soc.sendall(name.encode("utf8"))
        checkFound = soc.recv(1024).decode("utf8")
        if checkFound == "Found":
            winningGame = soc.recv(1024).decode("utf8")
            print(f"{name}'s winning game: {winningGame}")
        else:
            print(f"{name} is not existed")

    def check_username_showNote(soc):
        print("show username's show winning game:")
        name = input("Enter username: ")
        founded = False
        soc.sendall(name.encode("utf8"))
        checkFound = soc.recv(1024).decode("utf8")
        if checkFound == "Found":
            note = soc.recv(1024).decode("utf8")
            print(f"{name}'s note: {note}")
        else:
            print(f"{name} is not existed")

    def check_username_showall(soc):
        print("show username's all info")
        name = input("Enter username: ")
        founded = False
        soc.sendall(name.encode("utf8"))
        checkFound = soc.recv(1024).decode("utf8")
        if checkFound == "Found":
            temp = soc.recv(1024).decode("utf8")
            info = temp.split(';')
            # print(f"{name}'s online: {note}")
            print(f"{name}'s fullname: {info[2]}")
            print(f"{name}'s date of birth: {info[3]}")
            print(f"{name}'s winning game: {info[4]}")
            print(f"{name}'s note: {info[5]}")
            print(f"{name}'s online status: {info[6]}")
        else:
            print(f"{name} is not existed")

    choice = 0
    while choice != 8:
        print('\n1) find user.')
        print('2) check if user online.')
        print("3) show user's fullname.")
        print("4) show user's date of birth.")
        print("5) show user's winning game.")
        print("6) show user's note.")
        print("7) show user's all information.")
        print("8) go back.")
        choice = int(input('Enter your choice (1-8): '))
        soc.sendall(str(choice).encode("utf8"))
        if choice == 1:
            check_username_find(soc)
        elif choice == 2:
            check_username_online(soc)
        elif choice == 3:
            check_username_showfullname(soc)
        elif choice == 4:
            check_username_showdate(soc)
        elif choice == 5:
            check_username_showWinningGame(soc)
        elif choice == 6:
            check_username_showNote(soc)
        elif choice == 7:
            check_username_showall(soc)
        elif choice !=8:
            print("Your choice is invalid!")
        if choice !=8:
            buffer = input("Enter something to continue(anything): ")
        clearConsole()

def ChangePassword(soc):
    oldPassword = input('Enter your old password: ')
    newPassword = input('Enter your new password: ')
    list = [usernameLoginSuccessful[0], oldPassword, newPassword]
    soc.sendall(';'.join(list).encode("utf8"))
    message = soc.recv(1024).decode("utf8")
    if message == 'change password successful':
        print('Change password successful!!')
    else:
        print('wrong password')

def SetupInfo(soc):
    def SetFullname(soc):
        print()
        newUserName = input('Enter new full name: ')
        list = [usernameLoginSuccessful[0], newUserName]
        soc.sendall(';'.join(list).encode("utf8"))
        message = soc.recv(1024).decode("utf8")
        if message == 'Set successful':
            print('Set successful')
        else:
            print('set unsuccessful')

    def SetBirthday(soc):
        print()
        newUserName = input('Enter new birthday: ')
        list=[usernameLoginSuccessful[0], newUserName]
        soc.sendall(';'.join(list).encode("utf8"))
        message = soc.recv(1024).decode("utf8")
        if message == 'Set successful':
            print('Set successful')
        else:
            print('set unsuccessful')

    def SetNote(soc):
        print()
        newUserName = input('Enter new note: ')
        list=[usernameLoginSuccessful[0], newUserName]
        soc.sendall(';'.join(list).encode("utf8"))
        message = soc.recv(1024).decode("utf8")
        if message == 'Set successful':
            print('Set successful')
        else:
            print('set unsuccessful')

    choice = 0
    while choice != 4:
        print('1) Set fullname.')
        print('2) Set date of birth.')
        print('3) Set note.')
        print('4) Get back.')
        choice = int(input('Enter your choice: '))
        soc.sendall(str(choice).encode("utf8"))
        if choice == 1:
            SetFullname(soc)
        elif choice == 2:
            SetBirthday(soc)
        elif choice == 3:
            SetNote(soc)
        waiting2sAndCleanConsole()

#end after login section

#game play

def GamePlay(soc):
    clearConsole()
    
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
    
    createBoard()
    sendBoardtoServer()
    # soc.sendall(';'.join(list).encode("utf8"))
    # message = soc.recv(1024).decode("utf8")
    turnOrder = soc.recv(1024).decode("utf8")
    if turnOrder == "1":
        endGame = False
        while endGame == False:
            printTwoBoard()
            print("Your turn!")
            x = input("Enter your x position: ")
            y = input("Enter your y position: ")
            soc.sendall(";".join([x, y]).encode("utf8"))
            message = soc.recv(1024).decode("utf8")
            clearConsole() ################
            if message == "hit":
                print("Your bullet hit a ship!")
                print("You got another attack turn.")
                board2[int(x)][int(y)] = "D"
            elif message == "Miss":
                clearConsole()      ######################                
                print("Your bullet miss!")
                print("It's opponent's turn.")
                board2[int(x)][int(y)] = "M"
                messageOpponentTurn=""
                while messageOpponentTurn != "YourTurn":
                    printTwoBoard() #####################
                    positionOpponentBullet = soc.recv(1024).decode("utf8").split(";")
                    clearConsole()  ###############
                    oppoX = int(positionOpponentBullet[0])
                    oppoY = int(positionOpponentBullet[1])
                    print(f"Opponent' bullet position: X = {oppoX}, y= {oppoY}.")
                    messageOpponentTurn = soc.recv(1024).decode("utf8")
                    if messageOpponentTurn == "YouLose":
                        clearConsole() #######################
                        board1[oppoX][oppoY] = "D"
                        printTwoBoard()
                        print("Opponent hit all your ships!")
                        print("You Lose!")
                        requestToPlayAgainSignel = soc.recv(1024).decode("utf8")
                        print("Do you want to play again?")
                        choice = input("Enter your choice (y/n): ")
                        if choice == "n":
                            soc.sendall("endGame".encode("utf8"))
                            return
                        else:
                            soc.sendall("playAgain".encode("utf8"))
                        print("Waiting for accept playing again from opponent...")
                        messageOpponentPlayAgain = soc.recv(1024).decode("utf8")
                        if messageOpponentPlayAgain == "endGame":
                            endGame= True
                    elif messageOpponentTurn != "YourTurn":
                        # ban trung
                        board1[oppoX][oppoY] = "D" 
                        print("They hit your ship")
                    else:
                        board2[oppoX][oppoY] = "M" 
                        print("They miss your ship")
            elif message == "YouWin":
                clearConsole() ####################
                board2[int(x)][int(y)] = "D"
                printTwoBoard()
                print("Your bullet hit a ship!")
                print("Congratulation! you win the game.")
                print("Waiting for accept playing again from opponent...")
                waitingPlayAgainSignalFromOpponent = soc.recv(1024).decode("utf8")
                PlayAgainSignalFromOpponent = soc.recv(1024).decode("utf8")
                if PlayAgainSignalFromOpponent == 'endGame':
                    print("Opponent refuse to play again!")
                    print("The game will end right now")
                    endGame = True
                elif PlayAgainSignalFromOpponent == "Please send play again signal":
                    print("Do you want to play again?")
                    choice = input("Enter your choice (y/n): ")
                    if choice == "n":
                        soc.sendall("endGame".encode("utf8"))
                        return
                    else:
                        soc.sendall("playAgain".encode("utf8"))     
    #go second turn
    elif turnOrder == "2":
        print("Your opponent go first!")
        endGame = False
        messageOpponentTurn=""
        while messageOpponentTurn != "YourTurn":
            printTwoBoard() #########
            positionOpponentBullet = soc.recv(1024).decode("utf8").split(";")
            clearConsole() ##########
            oppoX = int(positionOpponentBullet[0])
            oppoY = int(positionOpponentBullet[1])
            print(f"Opponent' bullet position: X = {oppoX}, y= {oppoY}.")
            messageOpponentTurn = soc.recv(1024).decode("utf8")
            if messageOpponentTurn == "YouLose":
                clearConsole() #######################
                board1[oppoX][oppoY] = "D" 
                printTwoBoard()
                print("Opponent hit all your ships!")
                print("You Lose!")
                requestToPlayAgainSignel = soc.recv(1024).decode("utf8")
                print("Do you want to play again?")
                choice = input("Enter your choice (y/n): ")
                if choice == "n":
                    soc.sendall("endGame".encode("utf8"))
                    return
                else:
                    soc.sendall("playAgain".encode("utf8"))
                print("Waiting for accept playing again from opponent...")
                messageOpponentPlayAgain = soc.recv(1024).decode("utf8")
                if messageOpponentPlayAgain == "endGame":
                    endGame= True
            elif messageOpponentTurn != "YourTurn":
                # ban trung
                board1[oppoX][oppoY] = "D"  ####### xoa dong o duoi
                print("They hit your ship")
            else:
                board1[oppoX][oppoY] = "M"  ####### xoa dong o duoi
                print("They miss your ship")
        while endGame == False:
            printTwoBoard()
            print("Your turn!")
            x = input("Enter your x position: ")
            y = input("Enter your y position: ")
            soc.sendall(";".join([x,y]).encode("utf8"))
            message = soc.recv(1024).decode("utf8")
            clearConsole() ###############
            if message == "hit":
                print("Your bullet hit a ship!")
                print("You got another attack turn.")
                board2[int(x)][int(y)] = "D"
            elif message == "Miss":
                clearConsole()  ##########
                print("Your bullet miss!")
                print("It's opponent's turn.")
                board2[int(x)][int(y)] = "M"
                messageOpponentTurn = "" 
                while messageOpponentTurn != "YourTurn":
                    printTwoBoard() #########
                    positionOpponentBullet = soc.recv(1024).decode("utf8").split(";")
                    clearConsole() #######
                    oppoX = int(positionOpponentBullet[0])
                    oppoY = int(positionOpponentBullet[1])
                    print(f"Opponent' bullet position: X = {oppoX}, y= {oppoY}.")
                    messageOpponentTurn = soc.recv(1024).decode("utf8")
                    if messageOpponentTurn == "YouLose":
                        board1[oppoX][oppoY] = "D"
                        printTwoBoard()
                        print("Opponent hitted all your ships!")
                        print("You Lose!")
                        print("Do you want to play again?")
                        choice = input("Enter your choice (y/n): ")
                        if choice == "n":
                            soc.sendall("endGame".encode("utf8"))
                            return
                        else:
                            soc.sendall("playAgain".encode("utf8"))
                        print("Waiting for accept playing again from opponent...")
                        messageOpponentPlayAgain = soc.recv(1024).decode("utf8")
                        if messageOpponentPlayAgain == "endGame":
                            endGame= True
                    elif messageOpponentTurn != "YourTurn":
                        # ban trung
                        board1[oppoX][oppoY] = "D" 
                        print("they hit your ship")
                    else:
                        board1[oppoX][oppoY] = "M"
            elif message == "YouWin":
                clearConsole()
                board2[int(x)][int(y)] = "D"
                printTwoBoard()
                print("Your bullet hit a ship!")
                print("Congratulation! you win the game.")
                print("Waiting for accept playing again from opponent...")
                waitingPlayAgainSignalFromOpponent = soc.recv(1024).decode("utf8")
                PlayAgainSignalFromOpponent = soc.recv(1024).decode("utf8")
                if PlayAgainSignalFromOpponent == 'endGame':
                    print("Opponent refuse to play again!")
                    print("The game will end right now")
                    endGame = True
                elif PlayAgainSignalFromOpponent == "Please send play again signal":
                    print("Do you want to play again?")
                    choice = input("Enter your choice (y/n): ")
                    if choice == "n":
                        soc.sendall("endGame".encode("utf8"))
                        return
                    else:
                        soc.sendall("playAgain".encode("utf8"))            

if __name__ == "__main__":
    clearConsole()
    chooseSever()
    createClient()
