def main():
    files_to_scan_func()


def files_to_scan_func():
    with open("Resources\Backup.txt", "r") as f:
        files = f.readlines()
        i = 0
        while i < len(files):
            files[i] = files[i].replace("\n", "")
            print(files[i])
            i += 1
        print(files)





if __name__ == '__main__':
    main()
