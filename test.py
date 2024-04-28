import asyncio
import time
import digitalio
import board

async def check_button(button, button_name, last_press_time):
    debounce_delay = 0.2
    while True:
        if button.value and (time.time() - last_press_time) > debounce_delay:
            print(f"Button {button_name} Pressed")
            last_press_time = time.time()
            # Perform action
        await asyncio.sleep(0.01)  # yield control and reduce CPU usage

async def main():
    buttonA = digitalio.DigitalInOut(board.D23)
    buttonA.switch_to_input(pull=digitalio.Pull.DOWN)
    buttonB = digitalio.DigitalInOut(board.D24)
    buttonB.switch_to_input(pull=digitalio.Pull.DOWN)

    last_press_time_a = 0
    last_press_time_b = 0

    await asyncio.gather(
        check_button(buttonA, "A", last_press_time_a),
        check_button(buttonB, "B", last_press_time_b),
    )

asyncio.run(main())
