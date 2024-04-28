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
    last_a_press = 0
    last_b_press = 0
    debounce_time = 0.2  # 200 milliseconds

    while True:
        now = time.monotonic()
        if not buttonA.value and (now - last_a_press > debounce_time):
            print("Button A Pressed")
            last_a_press = now
        if not buttonB.value and (now - last_b_press > debounce_time):
            print("Button B Pressed")
            last_b_press = now
        await asyncio.sleep(0.05)  # Check buttons every 50 ms


# Main function to run the event loop
async def main():
    display_task = asyncio.create_task(update_display())
    buttons_task = asyncio.create_task(check_buttons())
    await asyncio.gather(display_task, buttons_task)

# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())
