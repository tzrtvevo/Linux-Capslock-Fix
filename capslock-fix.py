#!/usr/bin/env python3
import evdev
from evdev import UInput, ecodes as e
import select
import sys

device_path = 'insert device path here'

kbd = evdev.InputDevice(device_path)

ui = UInput(
    {{
        e.EV_KEY: kbd.capabilities()[e.EV_KEY],
        e.EV_MSC: [e.MSC_SCAN],
        e.EV_LED: [e.LED_NUML, e.LED_CAPSL, e.LED_SCROLLL],
    }},
    name="capslock-fixed",
)


kbd.grab()

try:
    while True:
        select.select([kbd.fd], [], [])
        for event in kbd.read():
            if event.type == e.EV_KEY and event.code == e.KEY_CAPSLOCK:
                if event.value == 1:
                    ui.write(e.EV_KEY, e.KEY_CAPSLOCK, 1)
                    ui.syn()
                    ui.write(e.EV_KEY, e.KEY_CAPSLOCK, 0)
                    ui.syn()
            else:
                ui.write(event.type, event.code, event.value)
                if event.type == e.EV_SYN:
                    ui.syn()
except KeyboardInterrupt:
    pass

finally:
    kbd.ungrab()
    ui.close()