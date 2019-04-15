import subprocess


def main():
    with open("Resources\\Temporary_Files\\Current_Network.txt") as file:
        f_full = file.read()
        print(f_full)
        if f_full != "":
            new = f_full.split("SSID")[1]
            new = new.split(": ")[1]
            current_network = new.split("\n")[0]
            print("Currently connected to -> " + current_network)


if __name__ == '__main__':
    subprocess.run("Resources\\Current_Network.bat")
    main()
