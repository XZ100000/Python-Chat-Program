import socket
import threading
import customtkinter as ctk
from cryptography.fernet import Fernet

# Server's IP and port
HOST = '0.0.0.0' # Your ip of your server/pc
PORT = 1234 # Your port

# Permanent encryption key
KEY = "ZzgRhgEgdBF2w5i8j_p3ip98QoLMSPdtJoKzg1bgESk="
cipher = Fernet(KEY.encode())

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")

        self.username = ""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.key_window()

    def key_window(self):
        self.clear_window()

        self.username_label = ctk.CTkLabel(self.master, text="Enter username:")
        self.username_label.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self.master)
        self.username_entry.pack(pady=10)

        self.connect_button = ctk.CTkButton(self.master, text="Connect", command=self.connect_to_server)
        self.connect_button.pack(pady=10)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def connect_to_server(self):
        self.username = self.username_entry.get().strip()
        if not self.username:
            return

        self.client_socket.connect((HOST, PORT))
        self.client_socket.send(cipher.encrypt(self.username.encode('utf-8')))

        self.clear_window()
        self.create_chat_window()

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def create_chat_window(self):
        self.chat_log = ctk.CTkTextbox(self.master, width=400, height=300)
        self.chat_log.pack(pady=10)

        self.message_entry = ctk.CTkEntry(self.master, width=300)
        self.message_entry.pack(side=ctk.LEFT, pady=10, padx=10)

        self.send_button = ctk.CTkButton(self.master, text="Send", command=self.send_message)
        self.send_button.pack(side=ctk.LEFT, pady=10, padx=10)

    def receive_messages(self):
        while True:
            try:
                encrypted_message = self.client_socket.recv(1024)
                if not encrypted_message:
                    break

                message = cipher.decrypt(encrypted_message).decode('utf-8')
                self.chat_log.insert(ctk.END, message + "\n")
                self.chat_log.yview(ctk.END)  # Scroll to the end of the chat log
            except:
                break

    def send_message(self):
        message = self.message_entry.get().strip()
        if not message:
            return

        encrypted_message = cipher.encrypt(message.encode('utf-8'))
        self.client_socket.send(encrypted_message)
        self.chat_log.insert(ctk.END, f"{self.username}: {message}\n")
        self.chat_log.yview(ctk.END)  # Scroll to the end of the chat log
        self.message_entry.delete(0, ctk.END)

    def on_closing(self):
        self.client_socket.close()
        self.master.destroy()

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    client = ChatClient(root)
    root.protocol("WM_DELETE_WINDOW", client.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
