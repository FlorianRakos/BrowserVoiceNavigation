import tkinter as tk
from tkinter import Label, Button, messagebox
import threading
import requests


class VoiceProcessingUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NOT CAPRICONS")
        self.root.configure(bg="#f0f0f0")

        self.status_label = Label(
            root, text="NOT CAPRICONS", font=("Helvetica", 30), bg="#f0f0f0"
        )
        self.status_label.pack(pady=20)

        self.record_button = Button(
            root,
            text="Record",
            command=self.record,
            font=("Helvetica", 22),
            bg="#4CAF50",
            fg="white",
        )
        self.record_button.pack(pady=10)

        self.quit_button = Button(
            root,
            text="Quit",
            command=self.quit_app,
            font=("Helvetica", 22),
            bg="#2196F3",
            fg="white",
        )
        self.quit_button.pack(pady=10)

        self.info_button = Button(
            root,
            text="Info",
            command=self.show_info,
            font=("Helvetica", 20),
            bg="#FFC107",
            fg="white",
        )
        self.info_button.pack(pady=10)

        # Initialize variables
        self.is_recording = False
        self.translation = ""

    def record(self):
        if not self.is_recording:
            self.status_label.config(text="Recording...")
            threading.Thread(target=self.start_recording).start()
            self.is_recording = True
        else:
            self.status_label.config(text="Recording already in progress...")

    def start_recording(self):
        requests.get("http://localhost:5000/reset")
        requests.get("http://localhost:5000/record")

        # Optionally, trigger translation and action execution here
        self.translate()

    def translate(self):
        translation_response = requests.get("http://localhost:5000/get_text")
        translation_data = translation_response.json()
        self.translation = translation_data.get("action", "")
        self.execute_action()

    def execute_action(self):
        self.status_label.config(text=f"Action: {self.translation}")
        # Implement logic to execute action based on self.translation

    def quit_app(self):
        if self.is_recording:
            self.status_label.config(text="Recording in progress. Cannot quit.")
        else:
            user_response = messagebox.askyesno("Quit", "Are you sure you want to quit")
            if user_response:
                self.status_label.config(text="Quitting...")
                self.root.destroy()  # Terminate the Tkinter application

    def show_info(self):
        messagebox.showinfo("Information", "Description on how the application works")


def main():
    root = tk.Tk()
    app = VoiceProcessingUI(root)
    root.geometry("800x600")
    root.mainloop()


if __name__ == "__main__":
    main()
