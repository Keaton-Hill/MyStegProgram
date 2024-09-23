import os
from PIL import Image
import hashlib

class Steganography:
    def hide_file(self, secret_file_path, cover_file_path, output_image_path, password=None):
        # Hash the password if provided
        password_hash = hashlib.sha256(password.encode()).hexdigest() if password else None

        # Open the cover image
        cover_image = Image.open(cover_file_path)
        cover_image = cover_image.convert("RGB")

        # Open the secret image
        secret_image = Image.open(secret_file_path)
        secret_image = secret_image.convert("RGB")

        # Ensure the secret image fits into the cover image
        if secret_image.size[0] * secret_image.size[1] > cover_image.size[0] * cover_image.size[1]:
            raise ValueError("Cover image is too small for the secret image.")

        # Modify the cover image to hide the secret image
        for y in range(secret_image.size[1]):
            for x in range(secret_image.size[0]):
                # Get the pixel values
                cover_pixel = list(cover_image.getpixel((x, y)))
                secret_pixel = list(secret_image.getpixel((x, y)))

                # Set the least significant bit of each color channel to the secret image pixel
                for i in range(3):  # RGB channels
                    cover_pixel[i] = (cover_pixel[i] & 0xFE) | (secret_pixel[i] >> (8 - 1))

                # Update the cover image pixel
                cover_image.putpixel((x, y), tuple(cover_pixel))

        # Save the modified image
        cover_image.save(output_image_path)

        # Save the password hash in a separate file if a password is set
        if password_hash:
            with open(output_image_path + '.hash', 'w') as f:
                f.write(password_hash)

    def extract_file(self, encoded_image_path, output_path, password=None):
        # Open the encoded image
        encoded_image = Image.open(encoded_image_path)
        encoded_image = encoded_image.convert("RGB")

        # Verify the password if it was set
        if password:
            hash_file_path = encoded_image_path + '.hash'
            if os.path.exists(hash_file_path):
                with open(hash_file_path, 'r') as f:
                    stored_hash = f.read().strip()
                if stored_hash != hashlib.sha256(password.encode()).hexdigest():
                    raise ValueError("Incorrect password for decryption. No file will be extracted.")

        # Create a new image for the secret file
        secret_image = Image.new("RGB", encoded_image.size)

        for y in range(secret_image.size[1]):
            for x in range(secret_image.size[0]):
                # Get the pixel values
                cover_pixel = list(encoded_image.getpixel((x, y)))

                # Extract the secret pixel from the least significant bit
                secret_pixel = [0, 0, 0]
                for i in range(3):
                    secret_pixel[i] = (cover_pixel[i] & 0x01) << (8 - 1)

                # Update the secret image pixel
                secret_image.putpixel((x, y), tuple(secret_pixel))

        # Save the secret image only if the password was correct
        secret_image.save(output_path)

        # Remove the hash file after successful extraction (optional)
        if os.path.exists(hash_file_path):
            os.remove(hash_file_path)
