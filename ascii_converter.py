# Main code to convert an image to ASCII characters
import math
from PIL import Image, ImageDraw, ImageFont


def image_to_ascii(path_image, output_file="output_ascii.jpg"):
    # ASCII characters used to build the output image (from darkest to lightest)
    ascii_chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]

    # Convert ASCII characters into a list
    charArray = list(ascii_chars)
    charLength = len(charArray)
    interval = charLength / 256  # Map pixel intensity to the number of ASCII chars

    # Scale down the image to make it smaller and more suitable for ASCII art
    scaleFactor = 0.1  # You can adjust this value
    oneCharWidth = 8  # Width of one ASCII character
    oneCharHeight = 16  # Height of one ASCII character

    def getChar(value):
        """Map grayscale intensity to an ASCII character."""
        return charArray[math.floor(value * interval)]

    # Open the image
    im = Image.open(path_image).convert("RGB")
    width, height = im.size
    im = im.resize((int(scaleFactor * width), int(scaleFactor * height *
                   (oneCharWidth / oneCharHeight))), Image.NEAREST)

    # Get pixel data
    width, height = im.size
    pixels = im.load()

    # Create new image for output ASCII art
    output_image = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color=(0, 0, 0))
    d = ImageDraw.Draw(output_image)

    # Use a monospaced font for ASCII art
    try:
        font = ImageFont.truetype('static/fonts/lucon.ttf', 15)  # Adjust the path as necessary
    except IOError:
        # Fall back to default font if truetype is unavailable
        font = ImageFont.load_default()

    # Generate ASCII art by drawing on the image
    for i in range(height):
        for j in range(width):
            # Get the RGB values of the pixel
            r, g, b = pixels[j, i]
            gray = int(r * 0.299 + g * 0.587 + b * 0.114)  # Convert to grayscale

            # Get corresponding ASCII character
            char = getChar(gray)

            # Draw the ASCII character on the output image
            d.text((j * oneCharWidth, i * oneCharHeight), char, font=font, fill=(r, g, b))

    # Save the output image as a .jpg
    output_image.save(output_file, 'JPEG')
