import asyncio
import subprocess
import digitalio
import board
import json
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789

# Configuration for display and hardware buttons
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
spi = board.SPI()
disp = st7789.ST7789(spi, cs=cs_pin, dc=dc_pin, width=135, height=240, x_offset=53, y_offset=40)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 18)

# Setup buttons
buttonA = digitalio.DigitalInOut(board.D23)
buttonA.switch_to_input(pull=digitalio.Pull.UP)
buttonB = digitalio.DigitalInOut(board.D24)
buttonB.switch_to_input(pull=digitalio.Pull.UP)

# Define the JSON-based menu structure
menu_json = """
{
  "Main Menu": [
    {
      "text": "Deploy HomeLab",
      "command": "P4wnP1_cli template deploy --full 'HomeLab'"
    },
    {
      "text": "Deploy Payload",
      "command": "P4wnP1_cli trigger send --group-name=payload --group-value=1"
    },
    {
      "text": "System Info",
      "command": "P4wnP1_cli trigger send --group-name=info --group-value=1"
    },
    {
        "text": "Sub Menu",
        "submenu": [
            {
            "text": "Sub Menu Item 1",
            "command": "echo 'Sub Menu Item 1 selected'"
            },
            {
            "text": "Sub Menu Item 2",
            "command": "echo 'Sub Menu Item 2 selected'"
            }
        ]
    },
    {
        "text": "Sub Menu 2",
        "submenu": [
            {
            "text": "Sub Menu Item 1",
            "command": "echo 'Sub Menu Item 1 selected'"
            },
            {
            "text": "Sub Menu Item 2",
            "command": "echo 'Sub Menu Item 2 selected'"
            }
            {
            "text": "Sub Menu Item 3",
            "command": "echo 'Sub Menu Item 3 selected'"
            },
            {
            "text": "Sub Menu Item 4",
            "command": "echo 'Sub Menu Item 4 selected'"
            },
            {
            "text": "Sub Menu Item 5",
            "command": "echo 'Sub Menu Item 5 selected'"
            }
        ]
    }
    {
      "text": "Utilities",
      "submenu": [
        {
          "text": "Shutdown",
          "command": "sudo shutdown now"
        },
        {
          "text": "Sub Menu Item 2",
          "command": "echo 'Sub Menu Item 2 selected'"
        }
      ]
    }
  ]
}
"""
menu_structure = json.loads(menu_json)

# Navigation state
current_menu = menu_structure["Main Menu"]
current_index = 0
menu_stack = []

# Drawing function
def draw_menu(menu_items, selected_index):
    image = Image.new("RGB", (disp.height, disp.width))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, disp.height, disp.width), outline=0, fill=0)
    
    # Add a 'Back' option if in a submenu
    if menu_stack:
        menu_items = [{"text": "< Back"}] + menu_items
    
    for i, item in enumerate(menu_items):
        text = item['text'] if 'text' in item else 'Unnamed Item'
        y_position = 30 + i * 20
        if i == selected_index:
            draw.text((10, y_position), f"> {text}", font=font, fill="#00FFFF")
        else:
            draw.text((10, y_position), text, font=font, fill="#00FFFF")
    
    disp.image(image, 90)

# Action execution function
def exec_action(item):
    if "command" in item:
        print(f"Executing {item['command']}")
        subprocess.run(item['command'], shell=True)

# Menu control function
async def menu_control():
    global current_menu, current_index
    while True:
        buttonA_pressed = not buttonA.value
        buttonB_pressed = not buttonB.value
        await asyncio.sleep(0.1)  # Debounce delay

        if buttonA_pressed:
            current_index = (current_index + 1) % len(current_menu + [{"text": "< Back"}] if menu_stack else current_menu)
            draw_menu(current_menu, current_index)
        if buttonB_pressed:
            if current_index == 0 and menu_stack:
                current_menu, current_index = menu_stack.pop()
                draw_menu(current_menu, current_index)
            else:
                adjusted_index = current_index - 1 if menu_stack else current_index
                selected_item = current_menu[adjusted_index]
                if "submenu" in selected_item:
                    menu_stack.append((current_menu, current_index))
                    current_menu = selected_item["submenu"]
                    current_index = 0
                    draw_menu(current_menu, current_index)
                elif "command" in selected_item:
                    exec_action(selected_item)

async def main():
    draw_menu(current_menu, current_index)
    await menu_control()

if __name__ == "__main__":
    asyncio.run(main())
