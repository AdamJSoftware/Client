import os
import sys


def OG(files):
    OG = files
    for lines in OG:
        if lines.__contains__("*"):
            OG.remove(lines)

    for lines in OG:
        try:
            newlines = lines.replace("\n", "")
            OG.remove(lines)
            OG.append(newlines)
        except:
            pass
    return OG


def backup2(filesAndSize, og):
    # print("OG2" + str(OG))
    newlist = []
    for files in filesAndSize:
        for remv in og:
            if str(files).__contains__(remv):
                newfile = str(files).replace(remv, str(""))
                firstchar = newfile[:1]
                if firstchar =='\\':
                    newfile = newfile[1:]
                    newlist.append(newfile)
            else:
                newlist.append(files)

    for lines in newlist:
        if lines == "\n":
            newlist.remove(lines)
            print("REMOVED")

    return newlist


def main():
    i = True
    files_to_scan_func(i)


def getsize(filename):
    try:
        st = os.stat(filename)
        return st.st_size
    except:
        return "AN ERROR OCCURRED. FILE NAME MAY BE TOO LONG"


def folder_func(path):
    list = []
    for name in os.listdir(path):
        newPath = os.path.join(path, name)
        list.append(newPath)
    return list


def folderorfile(file, filesAndSize, files):
    path = os.path.normpath(str(file))
    filesAndSize.append(file)
    if os.path.isdir(path):
        toBeAppended = folder_func(path)
        files.extend(toBeAppended)
    else:
        size = getsize(file)
        filesAndSize.append([size])


def files_to_scan_func(i):
    with open("Resources\Backup.txt", "r", encoding="utf-8-sig") as f:
        og = OG(f.readlines())

    with open("Resources\Backup.txt", "r", encoding="utf-8-sig") as f:
        filesAndSize = []
        filesToExculde = []
        f = f.readlines()
        files = f

    for file in files:
        try:
            file = file.replace("\n", "")
        except:
            pass
        if file.__contains__("*"):
            file = file.split("*")[1]
            filesToExculde.append(file)
            print("ADDED FILE TO EXCLUDE")
        if len(filesToExculde) == 0:
            folderorfile(file, filesAndSize, files)
        else:
            for i in filesToExculde:
                if i in file:
                    pass
                else:
                    folderorfile(file, filesAndSize, files)

    with open("Resources\Backup_SEND.txt", "w", encoding="utf-8") as f:
        for file in filesAndSize:
            f.write(str(file) + "\n")

    with open("Resources\Backup2.txt", "w", encoding="utf-8") as f:
        b2 = backup2(filesAndSize, og)
        for file in b2:
            f.write(str(file) + "\n")


if __name__ == '__main__':
    try:
        main()
    except:
        e = sys.exc_info()
        print(f'Error {e}')
