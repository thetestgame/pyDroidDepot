"""
This module provides classes for processing and handling notifications from a connected droid. 

It contains the DroidNotifyMessage class, which represents a notification message from the droid, and 
the DroidNotificationProcessor class, which handles incoming notifications from the droid and passes 
them to the appropriate handlers. The DroidNotificationProcessor class also includes methods for decoding 
incoming messages and verifying firmware versions.

This class is licensed under MIT.
"""

import logging
from droid.utils import hex_to_int
from droid.protocol import DroidCommandId
from droid.hardware import DroidFirmwareVersion

class DroidNotifyMessage(object):
    """
    Represents a notification message received from a droid.

    Attributes:
        message_size (int): The size of the message.
        unknown1 (int): An unknown integer value.
        command_id (int): The ID of the command associated with the notification.
        unknown3 (int): Another unknown integer value.
        message_data (str): The data associated with the notification.
    """

    def __init__(self, message_size: int, unknown1: int, command_id: int, unknown3: int, message_data: str):
        """
        Initializes a new instance of the DroidNotifyMessage class.

        Args:
            message_size (int): The size of the message.
            unknown1 (int): An unknown integer value.
            command_id (int): The ID of the command associated with the notification.
            unknown3 (int): Another unknown integer value.
            message_data (str): The data associated with the notification.
        """

        self.message_size = message_size
        self.unknown1 = unknown1
        self.command_id = command_id
        self.unknown3 = unknown3
        self.message_data = message_data

    def __str__(self) -> str:
        """
        Returns a string representation of the DroidNotifyMessage instance.

        Returns:
            str: A string representation of the DroidNotifyMessage instance.
        """

        return ('Size: %s, Unknown1: %s, Command Id: %s, Unknown2: %s, Data: %s' % (
            self.message_size, self.unknown1, self.command_id, self.unknown3, self.message_data))

class DroidNotificationProcessor(object):
    """
    Processes notification events from a connected droid.

    Attributes:
        droid (object): The connected droid instance.
    """

    def __init__(self, droid: object) -> None:
        """
        Initializes a new instance of the DroidNotificationProcessor class.

        Args:
            droid (object): The connected droid instance.
        """

        self.droid = droid

    def decode_notify_message(self, data: bytearray) -> DroidNotifyMessage:
        """
        Decodes an incoming message to a DroidNotifyMessage instance.

        Args:
            data (bytearray): The incoming message data.

        Returns:
            DroidNotifyMessage: A DroidNotifyMessage instance representing the incoming message.
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
        Processes notification events from the connected droid.

        Args:
            sender (object): The sender of the notification event.
            data (bytearray): The notification event data.
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