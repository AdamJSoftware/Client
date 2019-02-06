import os
import subprocess
import time

FNULL = open(os.devnull, 'w')


def Connected_To_Network():
    subprocess.run("Current_Network.bat", stdout= FNULL)
    with open("Current_Network.txt", encoding="(utf-16") as f:
        f = f.read()
        if f != "":
            f = f.split('\n')[0]
            print("Currently connected to -> " + f)
        else:
            f = ""
    with open("Saved_Network.txt") as SN:
        SN = SN.read()
        print("Current Server Network -> " + SN)
    if f == SN or SN == "Insert SSID":
        return True
    else:
        return False


try:
    os.remove("tmp.txt")
except:
    pass

try:
    f = open("Saved_Network.txt")
    f.read()
except:
    print("Resetting saved network")
    with open("Saved_Network.txt", "w") as f:
        f.write("Insert SSID")


if __name__ == '__main__':
    while True:
        if os.path.isfile("tmp.txt"):
            print('tmp.txt found')
        else:
            if Connected_To_Network() is True:
                subprocess.call(['python.exe', 'Client.py'])
                print('Connection lost to server...')
                print('Waiting for connection to the internet...')
            else:
                time.sleep(5)
