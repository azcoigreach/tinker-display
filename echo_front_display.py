import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import color565
from adafruit_rgb_display.st7789 import ST7789

# Setup display
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000

display = ST7789(
    board.SPI(),
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=240,
    height=1350,
    x_offset=0,
    y_offset=80,
)

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output(value=True)

# Display data
data = [
    "E-1C16 0.1.277 57C",
    "AUX1G:192.168.0.101",
    "100G1:192.168.100.101",
    "100G2:192.168.200.101"
]

# Font setup (adjust path as necessary)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 12)
except IOError:
    font = ImageFont.load_default()  # Fallback to default font if DejaVu Mono not found

def draw_display():
    # Clear display
    image = Image.new("RGB", (display.width, display.height))
    draw = ImageDraw.Draw(image)

    # Draw each line of data
    for i, line in enumerate(data):
        draw.text((10, 30 + i*20), line, font=font, fill=color565(0, 255, 255))

    # Rotate the image 90 degrees clockwise
    rotated_image = image.rotate(180, expand=True)

    # Display the rotated image
    display.image(rotated_image)

def main():
    draw_display()

if __name__ == "__main__":
    main()
