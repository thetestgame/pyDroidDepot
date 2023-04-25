"""
This is an example application that demonstrates how to connect to and control a 
SWGE Droid Depot Droid using the droid Python package.

This code randomly selects and plays sounds from the droid's audio library while connected 
over Bluetooth Low Energy (BLE).

The discover_droid function is used to find and connect to the droid. If the connection is 
successful, the script sets the volume to 20 and plays a randomly selected sound every 10-30 seconds.

This example code is licensed under the MIT license and is intended to demonstrate how to 
use the droid package. It is not intended for production use.
"""

import sys
sys.path.insert(0, '../')

from random import randrange
from droiddepot.connection import discover_droid, DroidCommandId
from droiddepot.script import DroidScripts
from time import sleep
from bleak import BleakError
import asyncio

async def main() -> None:
    """
    Main entry point into the example application
    """

    d = await discover_droid(retry=True)
    try:
        await d.connect()
        await d.audio_controller.set_volume(20)

        current_audio_index = 1
        while d.droid.is_connected:
            print("Playing sound id %s from bank 1" % current_audio_index)
            await d.audio_controller.play_audio(current_audio_index, 1, True)
            
            sleep(randrange(10, 30))
            current_audio_index += 1
            if current_audio_index > 5:
                current_audio_index = 1
            
    except OSError as err:
        print(f"Discovery failed due to operating system: {err}")
    except BleakError as err:
        print(f"Discovery failed due to Bleak: {err}")
    except KeyboardInterrupt as err:
        pass
    finally:
        print("Shutting down.")
        await d.disconnect()

# Main entry point into the example application
if __name__ == "__main__":
    asyncio.run(main())
