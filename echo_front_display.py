import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import color565
from adafruit_rgb_display import st7789

# Setup display
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000
spi = board.SPI()

display = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output(value=True)

padding_x = -10
padding_y = -10

# Display data
data = [
    "E-1C16 0.1.277 57C",
    "AUX1G:192.168.0.101",
    "100G1:192.168.100.101",
    "100G2:192.168.200.101"
]

# Font setup (adjust path as necessary)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 24)
except:
    font = ImageFont.load_default()  # Fallback to default font if DejaVu Mono not found
    print("Warning: DejaVu Mono font not found. Falling back to default font.")

def draw_display():
    # Set X
    x = padding_x

    # Clear display
    image = Image.new("RGB", (display.width, display.height))
    draw = ImageDraw.Draw(image)

    # Draw each line of data
    for i, line in enumerate(data):
        # getbox() returns a 2-tuple with the width and height of the text
        y = font.getbbox(line)[3] * i + padding_y
        draw.text((x, y), line, font=font, fill=color565(0, 255, 255))

    # Rotate the image 90 degrees clockwise
    rotated_image = image.rotate(90)

    # Display the rotated image
    display.image(rotated_image)

def main():
    draw_display()

if __name__ == "__main__":
    main()
