import tkinter as tk
from tkinter import Label, Button, messagebox
import threading
import requests

class VoiceProcessingUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NOT CAPRICONS")

        
        self.root.configure(bg="#f0f0f0")  

        
        self.status_label = Label(root, text="NOT CAPRICONS", font=("Helvetica", 30), bg="#f0f0f0")
        self.status_label.pack(pady=20)

        self.record_button = Button(root, text="Record", command=self.record, font=("Helvetica", 22), bg="#4CAF50", fg="white")
        self.record_button.pack(pady=10)

        self.reset_button = Button(root, text="Reset", command=self.reset, font=("Helvetica", 22), bg="#2196F3", fg="white")
        self.reset_button.pack(pady=10)

        self.info_button = Button(root, text="Info", command=self.show_info, font=("Helvetica", 20), bg="#FFC107", fg="white")
        self.info_button.pack(pady=10)

    def record(self):
        self.status_label.config(text="Recording...")
        threading.Thread(target=self.start_recording).start()

    def start_recording(self):
        requests.get("http://localhost:5000/reset")
        requests.get("http://localhost:5000/record")
        
    # Optionally, trigger translation and action execution here (advised by chatgbt)
        translation = self.translate()
        self.execute_action(translation)

    def translate(self):
        translation_response = requests.get("http://localhost:5000/get_text")
        translation_data = translation_response.json()
        translation = translation_data.get("action", "")
        return translation

    def execute_action(self, translation):
        self.status_label.config(text=f"Action: {translation}")

    def reset(self):
        self.status_label.config(text="Ready")
        requests.get("http://localhost:5000/reset")

    def show_info(self):
        messagebox.showinfo("Information", "Recording")

def main():
    root = tk.Tk()
    app = VoiceProcessingUI(root)
    root.geometr
