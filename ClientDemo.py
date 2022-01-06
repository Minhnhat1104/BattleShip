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


def chooseSever():
    global SERVER_ADDRESS
    SERVER_ADDRESS = input("Pls choose Sever address: ")
    global PORT
    PORT =  12121 #int(input("Pls choose a port: "))

messageList=[]

def createClient():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    try:
        soc.connect((SERVER_ADDRESS, PORT))
        inputmsg = input("Enter something: ")
        print(inputmsg)
        message = soc.recv(1024).decode("utf8").split(';')
        print(message)
    except:
        print("Server hasn't been install: ")
    finally:
        soc.close()
        
mesage="1234"
print(mesage.split(";"))