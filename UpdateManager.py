import requests
import os
import subprocess


def main():
    repository_version = requests.get('https://raw.githubusercontent.com/AdamJSoftware/Client/master/Version.txt')
    repository_version = repository_version.content.decode("utf-8")
    with open('Version.txt', 'r') as f:
        program_version = f.read()

    if repository_version[0] == program_version[0]:
        print('Client up-to-date')
    else:
        print('Updating client')
        client_update()

    subprocess.call(['python.exe', 'Main - UI.py'])


def client_update():
    client_version = requests.get("https://raw.githubusercontent.com/AdamJSoftware/Client/master/Version.txt")
    client_version = client_version.content.decode("utf-8")

    with open("Version.txt", "w") as f:
        f.write(client_version)

    client_repository = requests.get("https://raw.githubusercontent.com/AdamJSoftware/Client/master/Repository.txt")
    client_repository = client_repository.content.decode("utf-8")
    with open("Repository.txt", "w") as f:
        f.write(client_repository)

    remove_files(client_repository.split("\n"))
    write_new_files(client_repository.split("\n"))


def remove_files(client_repository):
    for index, file in enumerate(client_repository):
        try:
            if os.path.isfile(file):
                pass
            else:
                os.remove(file)
        except Exception as error:
            print(error)


def write_new_files(client_repository):
    for index, file in enumerate(client_repository):
        new_file = requests.get("https://raw.githubusercontent.com/AdamJSoftware/Client/master/" + file)
        new_file = new_file.content.decode("utf-8")
        with open(file, 'w') as f:
            f.write(new_file)


if __name__ == '__main__':
    main()
