import os
import subprocess
import time
import json
from threading import Thread

null = open(os.devnull, 'w')


class Default(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(1)
            subprocess.call(['python.exe', 'Client.py'])


def error_log(error):
    with open("Resources/ErrorLog.txt", 'a') as file:
        file.write(time.ctime() + "\n")
        file.write(str(error) + "\n" + "\n")


def error_print(error_message, error):
    print("SYSTEM ERROR - " + error_message + ": " + str(error))


def create_config():
    if os.path.isfile("config.json"):
        pass
    else:
        print("SYSTEM: Creating Config File...")
        config = {"computer_name": "", "ip": "",
                  "backup": [], "backup_exclude": []}
        with open('config.json', 'w') as f:
            json.dump(config, f)


def create_name():
    config = config_read()
    if config['computer_name'] == "":
        config['computer_name'] = input("What is the name of this computer: ")
        config_write(config)


def create_ip():
    config = config_read()
    if config['ip'] == "":
        config['ip'] = input("Please input IP address:")
        config_write(config)


def config_read():
    with open('config.json', 'r') as f:
        return json.load(f)


def config_write(data):
    with open('config.json', 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    create_config()
    create_name()
    create_ip()
    time.sleep(1)
    a = Default()
    a.start()
