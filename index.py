import time
import CHIP_IO.GPIO as GPIO # See Library: https://github.com/xtacocorex/CHIP_IO
from losantmqtt import Device

led = "GPIO1" #XIO-P2
button = "GPIO2" #XIO-P3
lightStatus = 0

GPIO.setup(led, GPIO.OUT)
GPIO.setup(button, GPIO.IN)

# Construct device
device = Device("my-device-id", "my-access-key", "my-access-secret")

def on_command(device, command):
    print("Command received.")
    print(command["name"])
    print(command["payload"])
    if command["name"] == "toggle":
        GPIO.output(led, lightStatus)


# Listen for commands.
device.add_event_observer("command", on_command)

# Connect to Losant.
device.connect(blocking=False)

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        device.loop()
        if device.is_connected():
            if GPIO.input(button):
                device.send_state({"button": 1})
                time.sleep(0.075) # Debounce button press
            else:
        time.sleep(0.03)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO
