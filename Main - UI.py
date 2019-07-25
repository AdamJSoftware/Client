import os
import subprocess
import time
from threading import Thread

null = open(os.devnull, 'w')

class Default(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            if os.path.isfile("Resources/Temporary_Files/tmp.txt"):
                pass
            else:
                time.sleep(1)
                os.system('cls')
                if get_network_connect() is True:
                    print('Connection lost to server...')
                    print('Waiting for connection to the internet...')
                    sn = sn_func()
                    print("Current Server Network -> " + sn)
                    ctn = connected_to_network()
                    if ctn is True:
                        time.sleep(1)
                        os.system('cls')
                        subprocess.call(['python.exe', 'Client - UI.py'])
                        os.system('cls')
                    else:
                        time.sleep(4)
                else:
                    time.sleep(1)
                    os.system('cls')
                    subprocess.call(['python.exe', 'Client - UI.py'])
                    os.system('cls')


def connected_to_network():
    f_full = subprocess.run('netsh wlan show interfaces', capture_output=True, text=True)
    f_full = f_full.stdout
    if f_full.__contains__(": connected"):
        try:
            new = f_full.split("SSID")[1]
            new = new.split(": ")[1]
            current_network = new.split("\n")[0]
            print("Currently connected to -> " + current_network)
        except Exception as error:
            error_print("Error while read current network", error)
            return False
    else:
        current_network = ""
    sn = sn_func()
    if current_network == sn or f_full.__contains__(sn) or sn == "Insert SSID":
        return True
    else:
        return False


def sn_func():
    with open("Resources/Temporary_Files/Saved_Network.txt") as SN:
        sn = SN.read()
        return sn


def error_log(error):
    with open("Resources/ErrorLog.txt", 'a') as file:
        file.write(time.ctime() + "\n")
        file.write(str(error) + "\n" + "\n")


def error_print(error_message, error):
    print("SYSTEM ERROR - " + error_message + ": " + str(error))


def create_resource_file(file_name, print_text, text):
    if os.path.isfile("Resources/" + file_name):
        pass
    else:
        print("SYSTEM: Creating " + print_text + "...")
        with open("Resources/" + file_name, "w+") as file_to_create:
            file_to_create.write(text)


def get_network_connect():
    with open("Resources/Config.txt", "r") as f:
        f = f.read()
        if f == "Network connect: True":
            return True
        else:
            return False


if os.path.isfile("Resources/Temporary_Files/tmp.txt"):
    os.remove("Resources/Temporary_Files/tmp.txt")
else:
    pass

if os.path.isdir("Resources/Temporary_Files"):
    pass
else:
    os.mkdir("Resources/Temporary_Files")


if __name__ == '__main__':
    create_resource_file("Temporary_Files/Saved_Network.txt", "Saved Network", "Insert SSID")
    create_resource_file("Backup.txt", "Backup Log", "")
    create_resource_file("Config.txt", "Config", "Network connect: True")
    create_resource_file("Temporary_Files/Client_Service.txt", "Client Service", "test")
    create_resource_file("Temporary_Files/Current_Network.txt", "Current Network", "")
    create_resource_file("Temporary_Files/Suspension.txt", "Suspension", "")
    time.sleep(3)
    a = Default()
    a.start()
