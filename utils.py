import pygame
from PIL import Image, ImageTk
import tkinter as tk

def play_music(music_file):
    pygame.mixer.init()  # Initialize the mixer
    pygame.mixer.music.load(music_file)  # Load the music file
    pygame.mixer.music.play(-1)  # Play it on loop

def stop_music():
    pygame.mixer.music.stop()  # Stop the music

def set_background(root, image_path):
    try:
        # Open the image
        image = Image.open(image_path)

        # Create a PhotoImage object
        background_image = ImageTk.PhotoImage(image)

        # Create a label with the background image
        background_label = tk.Label(root, image=background_image)
        background_label.place(relwidth=1, relheight=1)  # Cover the entire window

        # Keep a reference to avoid garbage collection
        background_label.image = background_image
    except Exception as e:
        print(f"Error loading background image: {e}")






