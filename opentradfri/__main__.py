"""Provide a CLI for Tradfri."""
import logging
from pprint import pprint
import sys

from .const import *  # noqa
from .coap_cli import api_factory
from .gateway import Gateway


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Call with {} <host> <key>'.format(sys.argv[0]))
        sys.exit(1)

    logging.basicConfig(level=logging.DEBUG)

    api = api_factory(sys.argv[1], sys.argv[2])
    gateway = Gateway(api)
    devices = gateway.get_devices()
    lights = [dev for dev in devices if dev.has_light_control]
    light = lights[0]
    groups = gateway.get_groups()
    group = groups[0]
    moods = gateway.get_moods()
    mood = moods[0]

    def dump_all():
        endpoints = gateway.get_endpoints()

        for endpoint in endpoints:
            parts = endpoint[1:].split('/')

            if not all(part.isdigit() for part in parts):
                continue

            pprint(api('get', parts))
            print()
            print()

    def dump_devices():
        pprint([d.raw for d in gateway.get_devices()])

    print()
    print("Example commands:")
    print("> devices")
    print("> light.light_control.lights")
    print("> light.light_control.set_dimmer(10)")
    print("> light.light_control.set_dimmer(254)")
    print("> light.light_control.set_xy_color(254)")
    print("> lights[1].light_control.set_dimmer(20)")
    print("> groups")
    print("> moods")
    print("> dump_devices()")
    print("> dump_all()")
