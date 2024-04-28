import asyncio
import board
import digitalio
from PIL import Image, ImageDraw
import adafruit_rgb_display.st7789 as st7789  # Adjust based on your display driver

# Setup for display
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Create the display object
disp = st7789.ST7789(
    board.SPI(),
    height=240,
    y_offset=40,
    rotation=90,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=24000000
)

# Setup buttons
buttonA = digitalio.DigitalInOut(board.D23)
buttonA.switch_to_input(pull=digitalio.Pull.UP)
buttonB = digitalio.DigitalInOut(board.D24)
buttonB.switch_to_input(pull=digitalio.Pull.UP)

# Function to update the display asynchronously
async def update_display():
    width = disp.width
    height = disp.height
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    while True:
        # Clear the display
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        draw.text((30, 40), "Hello, Async World!", fill="white")
        disp.image(image)
        await asyncio.sleep(1)  # Update every second

# Function to monitor button presses asynchronously
async def check_buttons():
    while True:
        if buttonA.value:
            print("Button A Pressed")
        if buttonB.value:
            print("Button B Pressed")
        await asyncio.sleep(0.1)  # Check buttons every 100 ms

# Main function to run the event loop
async def main():
    display_task = asyncio.create_task(update_display())
    buttons_task = asyncio.create_task(check_buttons())
    await asyncio.gather(display_task, buttons_task)

# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())
