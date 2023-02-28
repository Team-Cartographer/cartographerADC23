from PIL import Image
from math import sqrt

color_temps = {
'K26_30' : (249, 218, 241),
'K31_40' : (205, 109, 243),
'K41_50' : (178, 107, 242),
'K51_60' : (141, 105, 168),
'K61_70' : (106, 123, 167),
'K71_80' : (134, 145, 243),
'K81_90' : (179, 208, 250),
'K91_100' : (149, 210, 246),
'K101_110' : (144, 247, 248),
'K111_200' : (255, 255, 255),
'K201_225' : (255, 254, 226),
'K226_250' : (255, 255, 146),
'K251_275' : (248, 215, 137),
'K276_300' : (243, 174, 136),
'K301_325' : (239, 135, 132),
'K326_350' : (177, 130, 128)
}


def getBestColor(pixel: tuple) -> tuple:
    x2, y2, z2 = pixel
    min = 100000000000000000
    mincolor = None
    for key in color_temps:
        x1, y1, z1 = color_temps[key]
        testval = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
        if testval <= min:
            min = testval
            mincolor = key

    return mincolor



# Open the image
image = Image.open('C:/Users/ashwa/Desktop/image.png')
image = image.convert("RGB")
# Get the width and height of the image
width, height = image.size

# Create an empty list to store the RGB values
rgb_values = []

# Loop through each pixel in the image
for y in range(height):
    for x in range(width):
        # Get the RGB values of the pixel at (x, y)

        if y == height//2:
            print('Halfway There')
            print("Woah!!! Livin' on a prayer!")
        color = image.getpixel((x, y))
        rgb_values.append(getBestColor(color))

print(rgb_values)