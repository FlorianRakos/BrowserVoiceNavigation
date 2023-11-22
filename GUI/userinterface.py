import customtkinter
from customtkinter import CTk, Label, Button, messagebox
import tkinter
import tkinter.messagebox
import threading
import requests

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class VoiceProcessingUI:
    def __init__(self, root):
        self.root = root
        #self.root.title("NOT CAPRICONS")
        #self.root.configure(bg="#f0f0f0")  
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")
         # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        #self.status_label = Label(root, text="NOT CAPRICONS", font=("Helvetica", 30), bg="#f0f0f0")
        #self.status_label.pack(pady=20)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

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
        
        # Optionally, trigger translation and action execution here
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
    root = CTk()
    app = VoiceProcessingUI(root)
    root.geometry("800x600")
    root.mainloop()

if __name__ == "__main__":
    main()
