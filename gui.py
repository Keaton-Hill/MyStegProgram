import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from utils import set_background, play_music, stop_music
from stegCode import Steganography  # Import your steganography class
import os
import hashlib  # Import hashlib to use for password hashing

# Global variable to track music state
music_playing = True

class MyApp:
    def __init__(self, root):
        self.root = root
        self.secret_file_path = None
        self.cover_file_path = None
        self.steganography = Steganography()

        self.create_gui()

    def toggle_music(self):
        global music_playing
        if music_playing:
            stop_music()
        else:
            play_music('HoneyPie.mp3')
        music_playing = not music_playing

    def on_drop(self, event, label):
        file_path = event.data.strip('{}')  # Clean up any unwanted characters
        label.config(text=f"Selected: {file_path}")
        print(f"File dropped: {file_path}")

        if label == self.secret_label:
            self.secret_file_path = file_path
        elif label == self.cover_label:
            self.cover_file_path = file_path

    def process_files(self):
        if not self.secret_file_path or not self.cover_file_path:
            messagebox.showwarning("Missing Files", "Please drop both secret and cover files.")
            return

        # Prompt for password
        password = simpledialog.askstring("Set Password", "Enter a password for encryption (leave blank for no password):")

        # Prompt user for output file path
        output_image_path = filedialog.asksaveasfilename(defaultextension=".bmp", 
                                                          filetypes=[("BMP files", "*.bmp"), 
                                                                     ("All files", "*.*")])
        if not output_image_path:  # User cancelled the dialog
            return

        # Normalize the output file path
        output_image_path = os.path.normpath(output_image_path)

        # Debugging output
        print(f"Secret file path: {self.secret_file_path}")
        print(f"Cover file path: {self.cover_file_path}")
        print(f"Output image path: {output_image_path}")

        try:
            self.steganography.hide_file(self.secret_file_path, self.cover_file_path, output_image_path, password)
            messagebox.showinfo("Success", "Secret image hidden successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decrypt_file(self):
        # Prompt user to select the cover file for decryption
        cover_file_path = filedialog.askopenfilename(
            title="Select Cover File",
            filetypes=[("BMP files", "*.bmp"), ("All files", "*.*")]
        )

        if not cover_file_path:  # User cancelled the dialog
            return

        # Prompt for password
        password = simpledialog.askstring("Enter Password", "Enter password to decrypt:")
        
        if not password:
            messagebox.showwarning("No Password", "You must enter a password to decrypt.")
            return

        try:
            # Verify the password first
            stored_hash = None
            hash_file_path = cover_file_path + '.hash'
            if os.path.exists(hash_file_path):
                with open(hash_file_path, 'r') as f:
                    stored_hash = f.read().strip()
            
            password_hash = hashlib.sha256(password.encode()).hexdigest() if password else None
            if stored_hash != password_hash:
                raise ValueError("Incorrect password for decryption.")

            # If the password is correct, prompt for the output path
            output_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )

            if not output_path:  # User cancelled the dialog
                return

            # Proceed to decrypt the file
            self.steganography.extract_file(cover_file_path, output_path, password)
            messagebox.showinfo("Success", "File decrypted successfully!")

        except ValueError:
            messagebox.showwarning("Wrong Password", "Incorrect password! No file was decrypted.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_gui(self):
        set_background(self.root, 'Background.jpg')
        play_music('HoneyPie.mp3')

        mute_button = tk.Button(self.root, text="Mute", command=self.toggle_music, bg=self.root.cget("bg"), borderwidth=0)
        mute_button.pack(pady=10)

        # Secret file drag-and-drop
        self.secret_label = tk.Label(self.root, text="Drag Secret File Here", bg='lightgray', width=30, height=5, relief='raised')
        self.secret_label.pack(pady=10)
        self.secret_label.drop_target_register(DND_FILES)
        self.secret_label.dnd_bind('<<Drop>>', lambda event: self.on_drop(event, self.secret_label))

        # Cover file drag-and-drop
        self.cover_label = tk.Label(self.root, text="Drag Cover File Here", bg='lightgray', width=30, height=5, relief='raised')
        self.cover_label.pack(pady=10)
        self.cover_label.drop_target_register(DND_FILES)
        self.cover_label.dnd_bind('<<Drop>>', lambda event: self.on_drop(event, self.cover_label))

        go_button = tk.Button(self.root, text="GO", command=self.process_files, bg=self.root.cget("bg"), borderwidth=0)
        go_button.pack(pady=10)

        decrypt_button = tk.Button(self.root, text="Decrypt", command=self.decrypt_file, bg=self.root.cget("bg"), borderwidth=0)
        decrypt_button.pack(pady=10)

# Main entry point to run the application
if __name__ == "__main__":
    root = TkinterDnD.Tk()  # Use TkinterDnD for drag-and-drop support
    root.title("My Steganography Program")  # Set a title for the window
    root.geometry("800x600")  # Set initial window size
    app = MyApp(root)  # Create an instance of MyApp
    root.mainloop()

