import asyncio
import board
import digitalio
from PIL import Image
from adafruit_rgb_display import color565
from adafruit_rgb_display.st7789 import ST7789

# Configuration for CS, DC, and Reset pins:
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000  # High speed for better display performance

# Setup the display
display = ST7789(
    board.SPI(),
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
backlight.switch_to_output()

buttonA = digitalio.DigitalInOut(board.D23)
buttonA.switch_to_input(pull=digitalio.Pull.UP)
buttonB = digitalio.DigitalInOut(board.D24)
buttonB.switch_to_input(pull=digitalio.Pull.UP)

# Function to update the display asynchronously
async def update_display():
    while True:
        if buttonA.value and buttonB.value:
            backlight.value = False  # Turn off backlight
            display.fill(color565(0, 0, 0))  # Turn screen black
        else:
            backlight.value = True  # Turn on backlight
            if buttonB.value and not buttonA.value:  # Just button A pressed
                display.fill(color565(255, 0, 0))  # Red
            if buttonA.value and not buttonB.value:  # Just button B pressed
                display.fill(color565(0, 0, 255))  # Blue
            if not buttonA.value and not buttonB.value:  # None pressed
                display.fill(color565(0, 255, 0))  # Green
        
        await asyncio.sleep(0.1)  # Update at 10 Hz

# Main function to run the event loop
async def main():
    display_task = asyncio.create_task(update_display())
    await display_task

# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())
