import evdev
from evdev import UInput, ecodes as e
import select
import sys

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
keyboards = [
    d for d in devices
    if e.EV_KEY in d.capabilities()
    and e.KEY_CAPSLOCK in d.capabilities()[e.EV_KEY]
    and e.KEY_A in d.capabilities()[e.EV_KEY]
]

if not keyboards:
    print("No keyboards found")
    sys.exit(1)

print("Press any key to detect the keyboard...")

kbd = None
try:
    inputs, _, _ = select.select(keyboards, [], [])

    if inputs:
        kbd = inputs[0]
        print(f"Detected keyboard: {kbd.name} ({kbd.path})")
    else:
        print("No key pressed.")
        sys.exit(1)

except KeyboardInterrupt:
    print("\nExiting...")
    sys.exit(0)
    
print(f"Use path: {kbd.path}")