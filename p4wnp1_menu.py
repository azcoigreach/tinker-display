import asyncio
import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
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

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 20
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Setup buttons
buttonA = digitalio.DigitalInOut(board.D23)
buttonA.switch_to_input(pull=digitalio.Pull.UP)
buttonB = digitalio.DigitalInOut(board.D24)
buttonB.switch_to_input(pull=digitalio.Pull.UP)

# Menus
menu_items = [
    ("Network Scan", "P4wnP1_cli trigger send --group-name=scan --group-value=1"),
    ("Deploy Payload", "P4wnP1_cli trigger send --group-name=payload --group-value=1"),
    ("System Info", "P4wnP1_cli trigger send --group-name=info --group-value=1"),
    ("Shutdown", "sudo shutdown now")
]
current_index = 0
current_index = 0

def draw_menu(selected_index):
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    for i, item in enumerate(menu_items):
        # In draw_menu, change the line inside the loop to handle tuple:
        if i == selected_index:
            draw.text((10, 30 + i*20), f"> {item[0]}", font=font, fill="#00FFFF")  # Assume item is a tuple (displayText, command)
        else:
            draw.text((10, 30 + i*20), item[0], font=font, fill="#00FFFF")  # Display only the first element of the tuple

        # In exec_action, no change is needed as it already assumes item is a tuple and executes the second element.

    disp.image(image, rotation)

last_buttonA_state = False
last_buttonB_state = False

async def menu_control():
    global current_index, last_buttonA_state, last_buttonB_state
    while True:
        buttonA_pressed = buttonA.value and not last_buttonA_state
        buttonB_pressed = buttonB.value and not last_buttonB_state

        if buttonA_pressed:
            current_index = (current_index + 1) % len(menu_items)
            draw_menu(current_index)
        if buttonB_pressed:
            exec_action(current_index)

        last_buttonA_state = buttonA.value
        last_buttonB_state = buttonB.value
        await asyncio.sleep(0.1)

def exec_action(index):
    print(f"Executing {menu_items[index]}")
    subprocess.run(menu_items[index][1], shell=True)

async def main():
    draw_menu(current_index)
    await menu_control()

if __name__ == "__main__":
    asyncio.run(main())