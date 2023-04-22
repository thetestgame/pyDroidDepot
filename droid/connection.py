"""
DroidConnection is a class that represents a connection to a SWGE DroidDepot droid using BLE protocol. 
It provides methods for connecting and disconnecting to the droid, sending commands to it, and executing scripts. 
The class also contains instances of DroidAudioController, DroidMotorController, and DroidScriptEngine, 
which are used to control the droid's audio, motor, and script functions, respectively.

The DroidConnection class takes one argument, profile, which is a string representing the UUID of the BLE profile to connect to. 
After connecting to the droid using the connect method, the send_droid_command method can be used to send commands to the droid, 
and the execute_script method can be used to execute pre-defined scripts on the droid. 
The disconnect method can be used to disconnect from the droid.

This class is licensed under the MIT License.
"""

import asyncio
import logging
from time import sleep
from threading import Thread
from bleak import BleakScanner, BleakClient, BleakError
from droid.protocol import *
from droid.audio import DroidAudioController
from droid.motor import DroidMotorController
from droid.script import DroidScriptEngine, DroidScriptActions, DroidScripts

class DroidConnection(object):
    """
    Represents a connection to a SWGE DroidDepot droid.

    Args:
        profile (str): A string representing the UUID of the BLE profile to connect to.
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
        Starts the heartbeat event loop
        """

        asyncio.set_event_loop(loop)
        loop.run_forever()

    async def __send_heartbeat_command(self) -> None:
        """
        Sends our flash pairing led command to the droid. This command is used as both a connection status indicator as well
        as keeps our connection alive.
        """

        while self.droid.is_connected:
            await self.send_droid_command(DroidCommand.FlashPairingLed, "020001ff01ff0aff00")
            sleep(10)

    async def disconnect(self, silent: bool = False) -> None:
        """
        Disconnect from the Droid.
        """

        try:
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
        The build_droid_command function creates a bytearray that represents a command for a Droid. 
        It takes in a command_id (integer) and a data string, and returns the corresponding bytearray.

        The first byte of the bytearray represents the total length of the command in bytes. The second byte is 0x42 
        if the command id is 15, or 0x00 otherwise. The third byte is the command id itself. The fourth byte is the length 
        of the data string in bytes, plus 0x40. The remaining bytes are the data string itself, represented in hexadecimal format.

        If the data string is malformed, a ValueError is raised.

        Args:
            command_id (int): The command id to be included in the Droid command
            data (str): The data string to be included in the Droid command

        Returns:
            bytearray: The bytearray representation of the Droid command, with the given command id and data string.
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
        Sends a command to the Droid, composed of a command ID and optional data.

        If the data string is malformed, a ValueError is raised.

        Args:
            command_id (int): The ID of the command to send.
            data (str): Optional data to include in the command, as a string of hexadecimal digits.
        """

        command = self.build_droid_command(command_id, data)
        await self.droid.write_gatt_char(0x000d, bytearray.fromhex(command.hex()))

    async def send_droid_multi_command(self, command_id: int, data: str = "") -> None:
        """
        Sends a multi command to the Droid, composed of a command ID and optional data.

        If the data string is malformed, a ValueError is raised.

        Args:
            command_id (int): The ID of the command to send.
            data (str): Optional data to include in the command, as a string of hexadecimal digits.
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

    return True if candidate.name == "DROID" else False

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
                    logging.error("Droid discovery timed out.")
                    return
                else:
                    logging.warning("Droid discovery timed out. Retrying...")
                    continue
        except BleakError as err:
            logging.warning("Droid discovery failed. Retrying...")
            continue


    logging.info(f"Droid successfully discovered: [ {discovered_droid} ]")
    d = DroidConnection(discovered_droid)
    return d
