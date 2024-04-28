import asyncio
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import color565
from adafruit_rgb_display.st7789 import ST7789

# Setup display and buttons
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
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output(value=True)

buttonA = digitalio.DigitalInOut(board.D23)
buttonA.switch_to_input(pull=digitalio.Pull.UP)
buttonB = digitalio.DigitalInOut(board.D24)
buttonB.switch_to_input(pull=digitalio.Pull.UP)

menu_items = ["Network Scan", "Deploy Payload", "System Info", "Shutdown"]
current_index = 0

# Font setup
font = ImageFont.load_default()

def draw_menu(selected_index):
    # Clear display
    image = Image.new("RGB", (display.width, display.height))
    draw = ImageDraw.Draw(image)

    for i, item in enumerate(menu_items):
        if i == selected_index:
            draw.text((10, 30 + i*20), f"> {item}", font=font, fill=color565(255, 255, 255))
        else:
            draw.text((10, 30 + i*20), item, font=font, fill=color565(255, 255, 255))

    display.image(image)

# Initialize last button state to be not pressed
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
            execute_action(current_index)

        # Update the last button states
        last_buttonA_state = buttonA.value
        last_buttonB_state = buttonB.value

        await asyncio.sleep(0.1)  # Button check interval for debouncing

def execute_action(index):
    # Placeholder for action execution logic
    print(f"Executing {menu_items[index]}")

async def main():
    draw_menu(current_index)
    await menu_control()

if __name__ == "__main__":
    asyncio.run(main())
