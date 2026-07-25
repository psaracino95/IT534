import os
import xml.etree.ElementTree as ET
from PIL import Image, ExifTags, ImageFont, ImageDraw

image_dir = "images/"

# Load font and set up output folder
font_path = "fonts/Syne-Regular.otf"
font = ImageFont.truetype(font_path, 25)
output_folder = "images/output_files/"
#Make sure the dir is made for output!!!
os.makedirs(output_folder, exist_ok=True)

# Loop over all files in the directory
for filename in os.listdir(image_dir):
    #Ensures that the right file types are used
    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".bmp")):
        image_path = os.path.join(image_dir, filename)

        #Names the files after the previous 
        name = os.path.splitext(filename)[0]

        # Load image
        my_image = Image.open(image_path)
        print("Image dimensions:", my_image.size)

        # Safely extract EXIF data
        exif_data = {}
        raw_exif = my_image._getexif()

        if raw_exif:
            for key, value in raw_exif.items():
                if key in ExifTags.TAGS:
                    exif_data[ExifTags.TAGS[key]] = value

        # Initialize draw interface on the image object
        draw_text = ImageDraw.Draw(my_image)

        # Load font and draw text
        draw_text.text((50, 50), name, fill=(255, 0, 255), font=font)

        # Convert to RGB if needed (JPEG does not support RGBA transparency)
        if my_image.mode in ("RGBA", "P"):
            my_image = my_image.convert("RGB")

        # Save output
        output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + "_cleaned" + os.path.splitext(filename)[1])
        my_image.save(output_path)
        print(f"Successfully created and scrubbed {output_path}")

        