import os
import subprocess
import time
from threading import Thread

FNULL = open(os.devnull, 'w')


def connected_to_network():
    subprocess.run("Resources\Current_Network.bat", stdout= FNULL)
    with open("Resources\Temporary_Files\Current_Network.txt", encoding="(utf-16") as f:
        f = f.read()
        if f != "":
            f = f.split('\n')[0]
            print("Currently connected to -> " + f)
        else:
            f = ""
    SN = sn_func()
    if f == SN or SN == "Insert SSID":
        return True
    else:
        return False


def sn_func():
    with open("Resources\Temporary_Files\Saved_Network.txt") as SN:
        SN = SN.read()
        return SN

try:
    os.remove("Resources\Temporary_Files\\tmp.txt")
except:
    pass

try:
    os.remove("Resources\Temporary_Files\\Client_Service.txt")
except:
    pass

try:
    f = open("Resources\Temporary_Files\Saved_Network.txt")
    f.read()
except:
    print("Resetting saved network")
    try:
        with open("Resources\\Temporary_Files\\Saved_Network.txt", "w") as f:
            f.write("Insert SSID")
    except:
        pass

class Starter(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            if os.path.isfile("Resources\Temporary_Files\\tmp.txt"):
                pass
            else:
                if connected_to_network() is True:
                    os.system('cls')
                    subprocess.call(['python.exe', 'Client.py'])
                    os.system('cls')
                    print('Connection lost to server...')
                    print('Waiting for connection to the internet...')
                    SN = sn_func()
                    print("Current Server Network -> " + SN)
                else:
                    time.sleep(5)

class Check(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            try:
                with open("Resources\\Temporary_Files\\Client_Service.txt", "r") as f:
                    f.read()
                print('exiting service client')
                os._exit(1)
            except:
                pass


if __name__ == '__main__':
    a = Starter()
    b = Check()
    b.start()
    a.start()

