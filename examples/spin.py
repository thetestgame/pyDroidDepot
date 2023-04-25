"""
"""

import sys
sys.path.insert(0, '../')

from random import randrange
from droiddepot.connection import discover_droid, DroidCommandId
from droiddepot.motor import DroidMotorDirection, DroidMotorIdentifier
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

        current_direction = DroidMotorDirection.Forward
        while d.droid.is_connected:
            await d.motor_controller.send_motor_speed_command(current_direction, DroidMotorIdentifier.LeftMotor, 100, 300)
            sleep(50)  
            if current_direction == DroidMotorDirection.Forward:
                current_direction = DroidMotorDirection.Backwards
            else:
                current_direction = DroidMotorDirection.Forward
            
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
