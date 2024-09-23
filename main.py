import tkinter as tk
from tkinterdnd2 import TkinterDnD  # Ensure you're importing this
from gui import MyApp

if __name__ == "__main__":
    root = TkinterDnD.Tk()  # Use TkinterDnD for drag-and-drop support
    root.title("Keaton's Steganography Tool")  # Set the window title
    app = MyApp(root)  # Create an instance of MyApp
    root.mainloop()  # Start the main loop to run the application


