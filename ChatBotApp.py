import tkinter as tk
from tkinter import scrolledtext, messagebox, PhotoImage
import ChatManager
from ChatManager import *
from PIL import Image, ImageTk 

class ChatBotApp:
    def __init__(self, root):
        # Initialize the main window and set its properties
        # title, icon, size, and resizability
        self.root = root
        self.root.title("AlexAI - The future of AI")
        icon = PhotoImage(file="logo.png")
        self.root.iconphoto(True, icon)
        self.root.geometry("1224x822") # The same size as background
        self.chat_manager = ChatManager()

        # Load image, change size, and convert it to PhotoImage(so tkInter can use it)
        # Create a canvas to display the image
        self.bg_image = Image.open("terminal.jpeg").resize((1224, 822))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas = tk.Canvas(self.root, width=1224, height=822)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        self.create_widgets()
        self.load_previous_conversations()

    def create_widgets(self):

        # Helper text
        self.helper_text = tk.Label(
            self.canvas,
            text="To send a message, type Enter",
            font=("Courier", 14),
            bg="black",
            fg="lime",
        )
        self.canvas.create_window(500, 30, anchor="nw", window=self.helper_text)

        # Create a chat area (placed in canvas)
        self.chat_area = scrolledtext.ScrolledText(
        self.canvas,
        wrap=tk.WORD,
        font=("Courier", 14),
        bg="black",
        fg="lime",
        bd=0,
        highlightthickness=0
        )
        self.chat_area.vbar.pack_forget()
        self.canvas.create_window(350, 210, anchor="nw", window=self.chat_area, width=550, height=400)

        # Create input field
        self.entry_field = tk.Entry(self.canvas, width=50, font=("Courier", 14), fg="lime")
        self.canvas.create_window(420, 650, anchor="nw", window=self.entry_field)

        # Bind the Enter key to send the message
        self.entry_field.bind("<Return>", lambda event: self.send_message())

    # Makes chat area accessible to write in, adds the message, and then disables it again
    def display_message(self, role, message):
        if role != "system":
            self.chat_area['state'] = 'normal'
            self.chat_area.insert(tk.END, f"{role.capitalize()}: {message}\n\n")
            self.chat_area['state'] = 'disabled'
            self.chat_area.yview(tk.END)

    # Gets the user input, checks if it's empty, and sends it to the chat manager
    def send_message(self):
        user_input = self.entry_field.get().strip()
        if not user_input:
            messagebox.showwarning("Empty message", "Archintellect of the Knowledge does not respond to empty messages")
            return

        self.entry_field.delete(0, tk.END)
        self.display_message("user", user_input)

        response = self.chat_manager.chat(user_input)
        self.display_message("assistant", response)

    # Loads previous conversations from the chat manager and displays them in the chat area
    def load_previous_conversations(self):
        for msg in self.chat_manager.history:
            self.display_message(msg['role'], msg['content'])


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()

# Thanks to:
# FlatIcon for the icon used in the app
# <a href="https://www.flaticon.com/free-icons/melchor" title="melchor icons">Melchor icons created by Freepik - Flaticon</a>
# OpenAI for the openAI API
# <a href="https://openai.com/" title="OpenAI">OpenAI</a>
# iStockPhoto for the background image
# https://www.istockphoto.com/hu/fotó/régi-televízió-gm1211548970-351394174