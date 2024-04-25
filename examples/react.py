"""
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

    droid = await discover_droid(retry=True)
    try:
        async with droid as d:
            await d.audio_controller.set_volume(20)
            d.script_engine.start_beacon_reactions()

            while d.droid.is_connected:
                sleep(1)
            
    except OSError as err:
        print(f"Discovery failed due to operating system: {err}")
    except BleakError as err:
        print(f"Discovery failed due to Bleak: {err}")
    except KeyboardInterrupt as err:
        pass
    finally:
        print("Shutting down.")

# Main entry point into the example application
if __name__ == "__main__":
    asyncio.run(main())
