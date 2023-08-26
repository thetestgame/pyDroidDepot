"""
Copyright (c) Jordan Maxwell, All Rights Reserved.
See LICENSE file in the project root for full license information.

DroidConnection is a BLE class representing a connection to a SWGE DroidDepot droid. 
It includes methods for connecting, disconnecting, sending commands, and running scripts on the droid.

It also includes instances of DroidAudioController, DroidMotorController, and DroidScriptEngine 
to manage the droid's audio, motor, and script functions.
"""

import asyncio
import logging
from time import sleep
from threading import Thread
from bleak import BleakScanner, BleakClient
from droiddepot.protocol import *
from droiddepot.audio import DroidAudioController
from droiddepot.motor import DroidMotorController
from droiddepot.script import DroidScriptEngine, DroidScripts
from droiddepot.voice import DroidVoiceController
from droiddepot.notify import DroidNotificationProcessor
from droiddepot.hardware import DroidPersonalityIdentifier, DroidAffiliation

class DroidConnection(object):
    """
    Represents a connection to a SWGE DroidDepot droid.

    Args:
        profile (str): A string representing the UUID of the BLE profile to connect to.
        manufacturer_data (dict): A dictionary containing the manufacturer data of the droid being connected.
    """

    DroidServiceId = '09b600a0-3e42-41fc-b474-e9c0c8f0c801'

    def __init__(self, profile: str, manufacturer_data):
        """
        Initializes a new instance of the Droid class.

        Args:
            profile (str): A string representing the UUID of the BLE profile to connect to.
            manufacturer_data (dict): A dictionary containing the manufacturer data of the droid being connected.

        Attributes:
            droid: A BLE connection object for the droid.
            personality_id: The personality ID of the droid. Default is DroidPersonalityIdentifier.RUnit.
            affiliation_id: The affiliation ID of the droid. Default is DroidAffiliation.Scoundrel.
            audio_controller: An instance of the DroidAudioController class.
            script_engine: An instance of the DroidScriptEngine class.
            motor_controller: An instance of the DroidMotorController class.
            heartbeat_loop: An asyncio event loop used for the heartbeat thread.
            heartbeat_thread: A thread that runs the heartbeat_loop.
        """
        
        self.profile = profile
        self.droid = None
        self.manufacturer_data = manufacturer_data
        self.personality_id = DroidPersonalityIdentifier.RUnit
        self.affiliation_id = DroidAffiliation.Scoundrel

        self.audio_controller = DroidAudioController(self)
        self.script_engine = DroidScriptEngine(self)
        self.motor_controller = DroidMotorController(self)
        self.voice_controller = DroidVoiceController(self)
        self.notify_processor = DroidNotificationProcessor(self)

        self.heartbeat_loop = asyncio.new_event_loop()
        self.heartbeat_thread = None

    async def connect(self, silent: bool = False) -> None:
        """
        Connect to the Droid using BLE.
        """

        timeout = 0.0
        self.droid = BleakClient(self.profile)
        await self.droid.connect()
        await self.droid.start_notify(DroidBluetoothCharacteristics.DroidNotifyCharacteristic, self.notification_handler)

        while not self.droid.is_connected and timeout < 10:
            sleep (.1)
            timeout += .1

        connect_code = bytearray.fromhex("222001")
        await self.droid.write_gatt_char(0x000d, connect_code, False)
        await self.droid.write_gatt_char(0x000d, connect_code, False)

        droid_data = self.manufacturer_data[DisneyBLEManufacturerId.DroidManufacturerId]

        droid_data_len = len(droid_data)
        self.personality_id = droid_data[droid_data_len - 1]
        self.affiliation_id = (droid_data[droid_data_len - 2] - 0x80) / 2
        
        if not silent:
            await self.script_engine.execute_script(DroidScripts.DroidPairingSequence1)
            sleep(4)

        self.heartbeat_thread = Thread(target=self.__start_heartbeat_loop, args=(self.heartbeat_loop,), daemon=True)
        self.heartbeat_thread.start()
        asyncio.run_coroutine_threadsafe(self.__send_heartbeat_command(), self.heartbeat_loop)

    async def notification_handler(self, sender: object, data: bytearray) -> None:
        """
        Processes notification events from the connected droid and
        passes it to our notify message processor.
        """

        await self.notify_processor.handle_incoming_message(sender, data)

    def __start_heartbeat_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        """
        Starts the heartbeat event loop
        """

        asyncio.set_event_loop(loop)
        loop.run_forever()

    async def __send_heartbeat_command(self) -> None:
        """
        Sends a harmless unused command every 10 seconds to keep our connection to the droid alive even when not in use.
        """

        while self.droid.is_connected:
            await self.send_droid_command(DroidCommandId.ConnectionHeartbeat)
            sleep(10)

    async def disconnect(self, silent: bool = False) -> None:
        """
        Disconnect from the Droid.
        """

        if not self.droid.is_connected:
            return

        logging.info("Disconnecting from droiddepot")
        try:
            if not silent:
                await self.audio_controller.play_shutdown_audio()
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
        logging.debug('Sending command: %s' % command.hex())
        await self.droid.write_gatt_char(DroidBluetoothCharacteristics.DroidCommandCharacteristic, bytearray.fromhex(command.hex()))

    async def send_droid_multi_command(self, command_id: int, data: str = "") -> None:
        """
        Sends a multi command to the Droid, composed of a command ID and optional data.

        If the data string is malformed, a ValueError is raised.

        Args:
            command_id (int): The ID of the command to send.
            data (str): Optional data to include in the command, as a string of hexadecimal digits.
        """

        command = "44%s%s" % ("{:02d}".format(command_id), data)
        await self.send_droid_command(DroidCommandId.MultipurposeCommand, command)

    async def get_droid_firmware_information(self) -> None:
        """
        Requests the droid firmware information. Currently the contents of this data
        is unknown. Because of this this request only returns the raw data processed by the 
        notify command processor.
        """

        await self.send_droid_command(DroidCommandId.RetrieveFirmwareInformation)
        firemware_information = await self.notify_processor.wait_for_command_response(DroidCommandId.RetrieveFirmwareInformationResponse)
        if firemware_information == None:
            raise Exception('Failed to retrieve firmware information. No response given')
        return firemware_information

    async def set_pairing_led(self, state: bool) -> None:
        """
        Sets the active state of the droid's pairing led.

        Args:
            state (bool): State to set the led to
        """

        data = "00"
        data += "ff" if state else "00"
        await self.send_droid_command(DroidCommandId.SetPairingLedState, data)

    async def set_rgb_led(self, state: bool) -> None:
        """
        Sets the active state of the droid's onboard RGB led. Currently no droids exist that use this feature
        however its added for completeness.

        Args:
            state (bool): State to set the led to
        """

        data = "00"
        data += "ff" if state else "00"
        await self.send_droid_command(DroidCommandId.SetRGBLedState, data)

    async def flash_pairing_led(self, data: str) -> None:
        """
        Flashes the droids onboard pairing led. Currently the data required for this command has not been decoded. 

        An example piece of encoded data is "020001ff01ff0aff00". This hex encoded string will flash the pairing LED 10 times at 
        a rate of once per second.
        """

        await self.send_droid_command(DroidCommandId.FlashPairingLed, data)

async def discover_droids(retry: bool = False) -> list:
    """
    Scans for nearby Bluetooth devices manufactured by Disney and have the device name of "DROID" if any are found they will be
    converted to a DroidConnection and added to a list to return. If retry is False, the function will out after a set
    period of time and return without discovering any droids.

    Args:
        retry (bool): whether or not to continue scanning until a device is found or the function is interrupted

    Returns:
        a list of DroidConnection objects representing the discovered "DROID" Bluetooth devices if any. Otherwise an empty list
    """

    async with BleakScanner() as scanner:      
        await scanner.start()

        droid_connections = []

        droids = []
        while True:
            possible_droids = scanner.discovered_devices_and_advertisement_data
            if len(possible_droids) == 0:
                await asyncio.sleep(5)
                continue

            for possible_droid_address in possible_droids:
                ble_device, advertising_data = possible_droids[possible_droid_address]
                manufacturer_ids = list(advertising_data.manufacturer_data.keys()) if advertising_data.manufacturer_data != None else []

                if ble_device.name == "DROID" and DisneyBLEManufacturerId.DroidManufacturerId in manufacturer_ids:
                    droids.append((ble_device, advertising_data.manufacturer_data))
                    
            if len(droids) == 0:
                if not retry:
                    logging.error("Droid discovery failed. Retrying...")
                    await asyncio.sleep(5)
                    continue
                else:
                    logging.warning("Droid discovery failed. Retrying...")
                    await asyncio.sleep(5)
                    continue
            else:
                for discovered_droid in droids:
                    logging.info(f"Droid successfully discovered: [ {discovered_droid[0]} ]")
                    droid_connections.append(DroidConnection(*discovered_droid))
                break
    
    return droid_connections

async def discover_droid(retry: bool = False) -> DroidConnection:
    """
    Scans for nearby Bluetooth devices manufactured by Disney and have the device name of "DROID" and returns if found. If retry is True, the function will
    continue scanning until it finds a device or is interrupted. If retry is False, the function will time out after a
    set period of time and return without discovering a device.

    Args:
        retry (bool): whether or not to continue scanning until a device is found or the function is interrupted

    Returns:
        a DroidConnection object representing the discovered "DROID" Bluetooth device if any. Otherwise None
    """

    discovered_droids = await discover_droids(retry)
    return None if len(discovered_droids) == 0 else discovered_droids[0]