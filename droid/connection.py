"""
"""

import asyncio
from time import sleep
from threading import Thread
from bleak import BleakScanner, BleakClient, BleakError
from droid.protocol import *
from droid.audio import DroidAudioController
from droid.motor import DroidMotorController
from droid.script import DroidScriptEngine, DroidScriptActions, DroidScripts

class DroidConnection(object):
    """
    """

    def __init__(self, profile):
        """
        Initializes a new instance of the Droid class.

        Args:
            profile (str): A string representing the UUID of the BLE profile to connect to.
        """
        
        self.profile = profile
        self.droid = None

        self.audio_controller = DroidAudioController(self)
        self.script_engine = DroidScriptEngine(self)
        self.motor_controller = DroidMotorController(self)

        self.heartbeat_loop = asyncio.new_event_loop()
        self.heartbeat_thread = None

    async def connect(self, silent: bool = False) -> None:
        """
        Connect to the Droid using BLE.
        """

        timeout=0.0
        self.droid = BleakClient(self.profile)
        await self.droid.connect()
        while not self.droid.is_connected and timeout < 10:
            sleep (.1)
            timeout += .1

        connect_code = bytearray.fromhex("222001")
        await self.droid.write_gatt_char(0x000d, connect_code, False)
        await self.droid.write_gatt_char(0x000d, connect_code, False)
        
        if not silent:
            await self.script_engine.execute_script(DroidScripts.DroidPairingSequence1)
            sleep(4)

        self.heartbeat_thread = Thread(target=self.__start_heartbeat_loop, args=(self.heartbeat_loop,), daemon=True)
        self.heartbeat_thread.start()
        asyncio.run_coroutine_threadsafe(self.__send_heartbeat_command(), self.heartbeat_loop)

    def __start_heartbeat_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        """
        """

        asyncio.set_event_loop(loop)
        loop.run_forever()

    async def __send_heartbeat_command(self) -> None:
        """
        """

        while self.droid.is_connected:
            await self.send_droid_command(DroidCommand.FlashPairingLed, "020001ff01ff0aff00")
            sleep(10)

    async def disconnect(self, silent: bool = False) -> None:
        """
        Disconnect from the Droid.
        """

        try:
            await self.audio_controller.shutdown()

            if not silent:
                sound_bank = bytearray.fromhex("27420f4444001f09")
                await self.droid.write_gatt_char(0x000d, sound_bank)
                sound_selection = bytearray.fromhex("27420f4444001800")
                await self.droid.write_gatt_char(0x000d, sound_selection)
                sleep(3)
        finally:
            await self.droid.disconnect()

            if self.heartbeat_loop != None:
                self.heartbeat_loop.stop()

    def build_droid_command(self, command_id: int, data: str) -> bytearray:
        """
        """

        data_length = len(data) // 2
        header_length = 3

        if command_id == 15:
            byte2 = 0x42
        else:
            byte2 = 0x00

        total_length = data_length + header_length
        byte1 = total_length | 0x20
        byte3 = command_id
        byte4 = data_length + 0x40

        try:
            command_bytes = bytearray([byte1, byte2, byte3, byte4])
            command_bytes.extend(bytes.fromhex(data))
        except ValueError:
            raise ValueError("Failed to pack droid command (%s) with data (%s). Data is malformed" % (command_id, data))
        
        return command_bytes

    async def send_droid_command(self, command_id: int, data: str = "") -> None:
        """
        """

        command = self.build_droid_command(command_id, data)
        await self.droid.write_gatt_char(0x000d, bytearray.fromhex(command.hex()))

    async def send_droid_multi_command(self, command_id: int, data: str = "") -> None:
        """
        """

        command = "44%s%s" % ("{:02d}".format(command_id), data)
        await self.send_droid_command(DroidCommand.MultipurposeCommand, command)

def find_droid(candidate: object, data: object) -> bool:
    """
    Returns True if the candidate device name is "DROID", otherwise returns False.

    Args:
        candidate (Bleak Device): the Bluetooth device being scanned
        data (object): additional data collected during the scan (not used in this function)
    
    Returns:
        True if the candidate device name is "DROID", otherwise False
    """

    if candidate.name == "DROID":
        return True
    else:
        return False

async def discover_droid(retry: bool = False) -> DroidConnection:
    """
    Scans for nearby Bluetooth devices until a device named "DROID" is found. If retry is True, the function will
    continue scanning until it finds a device or is interrupted. If retry is False, the function will time out after a
    set period of time and return without discovering a device.

    Args:
        retry (bool): whether or not to continue scanning until a device is found or the function is interrupted

    Returns:
        a DroidConnection object representing the discovered "DROID" Bluetooth device if any. Otherwise None
    """

    discovered_droid = None

    while retry and discovered_droid is None:
        try:
            discovered_droid = await BleakScanner.find_device_by_filter(find_droid)
            if discovered_droid is None:
                if not retry:
                    print("Droid discovery timed out.")
                    return
                else:
                    print("Droid discovery timed out. Retrying...")
                    continue
        except BleakError as err:
            print("Droid discovery failed. Retrying...")
            continue


    print (f"Astromech successfully discovered: [ {discovered_droid} ]")
    d = DroidConnection(discovered_droid)
    return d
