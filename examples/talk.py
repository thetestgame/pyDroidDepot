"""
"""

import sys
sys.path.insert(0, '../')

from random import randrange
from droid.connection import discover_droid, DroidCommand
from droid.script import DroidScripts
from time import sleep
from bleak import BleakError
import asyncio

async def main() -> None:

    d = await discover_droid(retry=True)
    
    try:
        await d.connect()
        while d.droid.is_connected:
            await d.audio_controller.set_volume(20)
            await d.script_engine.execute_script(randrange(1, 7))
            sleep(2)
            await d.motor_controller.center_unit_head()
            
            sleep(randrange(10, 30))
            
    except OSError as err:
        print(f"Discovery failed due to operating system: {err}")
    except BleakError as err:
        print(f"Discovery failed due to Bleak: {err}")
    except KeyboardInterrupt as err:
        pass
    finally:
        print("\nShutting down.")
        await d.disconnect(silent=True)

if __name__ == "__main__":
    asyncio.run(main())
