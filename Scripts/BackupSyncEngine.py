import os


def main():
    with open(os.path.join('Resources', 'GETFILES.txt'), "r", encoding="utf-8-sig") as GF:
        GF = GF.readlines()
    with open(os.path.join('Resources', 'Backup_SEND.txt'), "r", encoding="utf-8-sig") as BS:
        BS = BS.readlines()

    FTS = []

    for file in GF:
        for line in BS:
            if line.__contains__(file):
                FTS.append(line)
                FTS.append(file)

    for line in FTS:
        print(line)

    with open(os.path.join('Resources', 'FTS.txt'), "w", encoding="utf-8") as f:
        for file in FTS:
            file = file.replace('\\', '/')
            f.write(file)


if __name__ == '__main__':
    main()
