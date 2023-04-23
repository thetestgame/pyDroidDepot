"""
"""

import sys
sys.path.insert(0, '../')

from random import randrange
from droid.connection import discover_droid, DroidCommandId
from droid.script import DroidScripts
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
        
        while d.droid.is_connected:
            await d.script_engine.execute_script(randrange(1, 7))
            sleep(2)
            await d.motor_controller.center_head()
            
            sleep(randrange(10, 30))
            
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
