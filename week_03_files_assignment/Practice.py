# from PIL import Image
# from PIL import ExifTags
# from PIL import ImageFont
# from PIL import ImageDraw


# my_image = Image.open("images/clancy_stuart.jpg")
# print(my_image.size)

# exif_data = {}
# for key, value in my_image._getexif().items():
#     if key in ExifTags.TAGS:
#         exif_data[ExifTags.TAGS[key]] = value

# ##print(exif_data)

# draw_text= ImageDraw.Draw(my_image)
# font = ImageFont.truetype("fonts/Syne-Regular.otf", 16)
# draw_text.text((25,50), "Practice", (255, 255, 255), font)
# my_image.save("sample-output.jpg")