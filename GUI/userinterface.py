import tkinter as tk
from tkinter import Label, ttk, messagebox
import threading
import requests
import keyboard


class VoiceProcessingUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BROWSER VOICE NAVIGATION")
        self.root.configure(bg="#f0f0f0")

        # Create a style for consistent button styling
        self.style = ttk.Style()
        self.style.configure(
            "Accent.TButton",
            font=("Helvetica", 14),
            background="black",
            borderwidth=2,
            relief="raised",
        )

        self.status_label = Label(
            root, text="BROWSER VOICE NAVIGATION", font=("Helvetica", 30), bg="#f0f0f0"
        )
        self.status_label.pack(pady=20)

        self.record_button = ttk.Button(
            root,
            text="Record",
            command=self.record,
            style="Accent.TButton",
        )
        self.record_button.pack(pady=10)

        self.reset_button = ttk.Button(
            root,
            text="Reset",
            command=self.reset,
            style="Accent.TButton",
        )
        self.reset_button.pack(pady=10)

        self.quit_button = ttk.Button(
            root,
            text="Quit",
            command=self.quit_app,
            style="Accent.TButton",
        )
        self.quit_button.pack(pady=10)

        self.info_button = ttk.Button(
            root,
            text="Info",
            command=self.show_info,
            style="Accent.TButton",
        )
        self.info_button.pack(pady=10)

        # Initialize variables
        self.is_recording = False
        self.translation = ""

        # Start listening for key presses
        keyboard.on_press_key("s", self.start_recording)
        if not self.start_recording:
            self.status_label.config(text="Recording...")
       
        keyboard.on_press_key("r", self.reset)
        keyboard.on_press_key("q", self.quit_app)
        keyboard.on_press_key("i", self.show_info)

    def record(self):
        if not self.is_recording:
            self.status_label.config(text="Recording...")
            threading.Thread(target=self.start_recording).start()
            self.is_recording = True
        else:
            self.status_label.config(text="Recording already in progress...")

    def start_recording(self, _=None):
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

        # Stop recording after executing the action
        self.stop_recording()

    def reset(self, _=None):
        self.status_label.config(text="Ready")
        requests.get("http://localhost:5000/reset")

    def quit_app(self, _=None):
        if self.is_recording:
            self.status_label.config(text="Recording in progress. Cannot quit.")
        else:
            user_response = messagebox.askyesno("Quit", "Are you sure you want to quit")
            if user_response:
                self.status_label.config(text="Quitting...")
                self.root.destroy()  

    def show_info(self, _=None):
        messagebox.showinfo("Information", "It's up to you to use the keyboard or clicks")

    def stop_recording(self):
        self.is_recording = False

def main():
    root = tk.Tk()
    app = VoiceProcessingUI(root)
    root.geometry("800x600")
    root.mainloop()

if __name__ == "__main__":
    main()

#  if not self.start_recording:
           # self.status_label.config(text="BROWSER VOICE NAVIGATTION")