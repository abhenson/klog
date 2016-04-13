#! /usr/bin/env python
import asyncio, evdev, datetime, os

base_dir = os.path.abspath(os.path.dirname(__file__))
mouse = evdev.InputDevice('/dev/input/event4')
keybd = evdev.InputDevice('/dev/input/event3')
now = datetime.datetime.now().isoformat()
with open(os.path.join(base_dir,'logs') + '/' + now + '.log', 'a') as f:

	async def print_events(device):
	    async for event in device.async_read_loop():
	        if event.type == evdev.ecodes.EV_KEY:
	            f.write('{}\n'.format(evdev.categorize(event)))

	for device in mouse, keybd:
	    asyncio.ensure_future(print_events(device))

	loop = asyncio.get_event_loop()
	loop.run_forever()
