import requests
import os
import subprocess


def main():
    repository_version = requests.get('https://raw.githubusercontent.com/AdamJSoftware/Client/master/Version.txt')
    with open('Version.txt', 'r') as f:
        program_version = f.read()

    if repository_version.content[0] == program_version[0]:
        print('Client up-to-date')
    else:
        print('Updating client')
        client_update()

    subprocess.call(['python.exe', 'Main - UI.py'])


def client_update():
    client_repository = requests.get("https://raw.githubusercontent.com/AdamJSoftware/Client/master/Version.txt")

    with open("Repository.txt", "w") as f:
        f.write(client_repository.content)

    remove_files(client_repository.content)


def remove_files(client_repository):
    for index, file in enumerate(client_repository):
        if os.path.isfile(file):
            pass
        else:
            os.remove(file)


def write_new_files(client_repository):
    for index, file in enumerate(client_repository):
        new_file = requests.get("https://raw.githubusercontent.com/AdamJSoftware/Client/master/" + file)
        with open(file, 'w') as f:
            f.write(new_file.content)


if __name__ == '__main__':
    main()
