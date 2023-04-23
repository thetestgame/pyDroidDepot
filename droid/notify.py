"""
This class is licensed under MIT.
"""

import logging
from droid.utils import hex_to_int
from droid.protocol import DroidCommandId
from droid.hardware import DroidFirmwareVersion

class DroidNotifyMessage(object):
    """
    """

    def __init__(self, message_size: int, unknown1: int, command_id: int, unknown3: int, message_data: str):
        """
        """

        self.message_size = message_size
        self.unknown1 = unknown1
        self.command_id = command_id
        self.unknown3 = unknown3
        self.message_data = message_data

    def __str__(self) -> str:
        """
        """

        return ('Size: %s, Unknown1: %s, Command Id: %s, Unknown2: %s, Data: %s' % (
            self.message_size, self.unknown1, self.command_id, self.unknown3, self.message_data))

class DroidNotificationProcessor(object):
    """
    """

    def __init__(self, droid: object) -> None:
        """
        """

        self.droid = droid

    def decode_notify_message(self, data: bytearray) -> DroidNotifyMessage:
        """
        Decodes the incoming message to a DroidNotifyMessage instance
        """

        hex_data = data.hex()
        message_size = hex_to_int(hex_data[:2]) - 0x1f
        unknown1 = hex_to_int(hex_data[2:4])
        command_id = hex_to_int(hex_data[4:6])
        unknown3 = hex_to_int(hex_data[6:8])
        message_data = hex_data[8:]

        if len(data) != message_size:
            raise ValueError('Received truncated packet. Expected %s, got %s' % (len(data), message_size))

        return DroidNotifyMessage(message_size, unknown1, command_id, unknown3, message_data)

    async def handle_incoming_message(self, sender: object, data: bytearray) -> None:
        """
        Processes notification events from the connected droid
        """

        try:
            message = self.decode_notify_message(data)
            await self.__process_incoming_message(message)
        except ValueError as e:
            logging.error('Failed to process notification message with data %s. Data is malformed' % (data.hex()))
            logging.error(e, exc_info=True)

    async def __process_incoming_message(self, message: DroidNotifyMessage) -> None:
        """
        Processes the parsed command message from the connected droid passing it
        to the available command handlers.
        """

        if not DroidCommandId.valid_command(message.command_id):
            logging.warning('Received unknown command %s. Ignoring' % message.command_id)
            return
        
        if message.command_id == DroidCommandId.RetrieveFirmwareInformationResponse:
            await self.__verify_firmware_version(message)
        else:
            logging.warning('No handler present for droid command: %s' % DroidCommandId(message.command_id).name)

    async def __verify_firmware_version(self, message: DroidNotifyMessage) -> None:
        """
        Checks if the firmware version received from our droid matches the expected firmware version
        """

        if message.message_data != DroidFirmwareVersion:
            raise Exception('Possibly incomaptible droid detected. Possibly a new firmware version.')